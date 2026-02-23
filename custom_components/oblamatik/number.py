import logging
from typing import Any

import aiohttp
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfVolumeFlowRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.info("Setting up Oblamatik number entities")
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating number entities for {len(devices)} devices")
    else:
        devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
            }
        ]
    numbers = []
    for device in devices:
        numbers.extend(
            [
                OblamatikTemperatureNumber(hass, device),
                OblamatikFlowNumber(hass, device),
            ]
        )
    async_add_entities(numbers, True)


class OblamatikBaseNumber(NumberEntity):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__()
        self._hass = hass
        self._device = device
        self._host = device["host"]
        self._port = device.get("port", 80)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=device.get("name", f"Oblamatik ({self._host})"),
            manufacturer="KWC",
            model="TLC15F",
        )
        self._attr_available = True

    async def _post_tlc(self, temperature: float, flow: float, changed: bool) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = f"temperature={temperature}&flow={flow}&changed={1 if changed else 0}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/api/tlc/1/", data=data, headers=headers, timeout=5
                ) as response:
                    success = response.status == 200
                    if success:
                        _LOGGER.info(
                            f"Successfully sent TLC command: temp={temperature}, flow={flow}"
                        )
                    else:
                        _LOGGER.warning(f"TLC command failed: {response.status}")
                    return success
        except Exception as e:
            _LOGGER.error("Error sending TLC command: %s", e)
            return False


class OblamatikTemperatureNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_temperature_number"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_native_min_value = 4.0
        self._attr_native_max_value = 80.0
        self._attr_native_step = 1.0
        self._attr_native_value = 38.0

    async def _get_current_flow(self) -> float | None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_url}/api/tlc/1/state/", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "flow" in data:
                            return float(data["flow"])
                        elif "flow_rate" in data:
                            return float(data["flow_rate"])
                        else:
                            _LOGGER.warning(f"Flow not found in response: {data}")
                            return None
                    else:
                        _LOGGER.warning(f"Failed to get state: {response.status}")
                        return None
        except Exception as e:
            _LOGGER.error("Error getting current flow: %s", e)
            return None

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.info(f"Setting temperature to {value}°C")
        self._attr_native_value = value
        current_flow = await self._get_current_flow()
        if current_flow is None:
            current_flow = 0.0
            _LOGGER.warning(f"Could not get current flow, using fallback: {current_flow} L/min")
        if await self._post_tlc(value, current_flow, True):
            _LOGGER.info(
                f"Temperature set successfully to {value}°C with flow {current_flow} L/min"
            )
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set temperature")


class OblamatikFlowNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow_number"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water"
        self._attr_native_min_value = 0.0
        self._attr_native_max_value = 10.0
        self._attr_native_step = 0.1
        self._attr_native_value = 0.0

    async def _get_current_temperature(self) -> float | None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_url}/api/tlc/1/state/", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "temperature" in data:
                            return float(data["temperature"])
                        elif "temp" in data:
                            return float(data["temp"])
                        else:
                            _LOGGER.warning(f"Temperature not found in response: {data}")
                            return None
                    else:
                        _LOGGER.warning(f"Failed to get state: {response.status}")
                        return None
        except Exception as e:
            _LOGGER.error("Error getting current temperature: %s", e)
            return None

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.info(f"Setting flow rate to {value} L/min")
        self._attr_native_value = value
        current_temp = await self._get_current_temperature()
        if current_temp is None:
            current_temp = 38.0
            _LOGGER.warning(f"Could not get current temperature, using fallback: {current_temp}°C")
        if await self._post_tlc(current_temp, value, True):
            _LOGGER.info(
                f"Flow rate set successfully to {value} L/min with temperature {current_temp}°C"
            )
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set flow rate")
