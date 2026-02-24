import logging
from typing import Any

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfVolumeFlowRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.info("Setting up Oblamatik sensors")
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating sensors for {len(devices)} devices")
    else:
        devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
                "type": entry.data.get("device_type", "unknown"),
                "model": entry.data.get("model", "Unknown"),
            }
        ]
    sensors = []
    for device in devices:
        device_type = device.get("type", "unknown")
        if device_type == "kitchen":
            sensors.extend(
                [
                    OblamatikTemperatureSensor(hass, device),
                    OblamatikFlowSensor(hass, device),
                    OblamatikStatusSensor(hass, device),
                    OblamatikWaterFlowSensor(hass, device),
                    OblamatikRequiredTemperatureSensor(hass, device),
                ]
            )
        elif device_type in ["bath", "shower"]:
            sensors.extend(
                [
                    OblamatikTemperatureSensor(hass, device),
                    OblamatikCurrentTemperatureSensor(hass, device),
                    OblamatikFlowSensor(hass, device),
                    OblamatikRequiredTemperatureSensor(hass, device),
                    OblamatikRequiredFlowSensor(hass, device),
                    OblamatikStatusSensor(hass, device),
                    OblamatikWaterFlowSensor(hass, device),
                    OblamatikBathFaucetSensor(hass, device),
                    OblamatikBathButtonSensor(hass, device),
                    OblamatikFlowRateLiterPerHourSensor(hass, device),
                ]
            )
        else:
            sensors.extend(
                [
                    OblamatikTemperatureSensor(hass, device),
                    OblamatikCurrentTemperatureSensor(hass, device),
                    OblamatikFlowSensor(hass, device),
                    OblamatikRequiredTemperatureSensor(hass, device),
                    OblamatikRequiredFlowSensor(hass, device),
                    OblamatikStatusSensor(hass, device),
                    OblamatikWaterFlowSensor(hass, device),
                    OblamatikBathFaucetSensor(hass, device),
                    OblamatikBathButtonSensor(hass, device),
                    OblamatikFlowRateLiterPerHourSensor(hass, device),
                ]
            )
    async_add_entities(sensors, True)


class OblamatikBaseSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__()
        self._hass = hass
        self._device = device
        self._host = device["host"]
        self._port = device.get("port", 80)
        self._device_type = device.get("type", "unknown")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=device.get("name", f"Oblamatik ({self._host})"),
            manufacturer="KWC/Viega/Crosswater",
            model=device.get("model", "Unknown"),
        )
        self._attr_available = True

    async def _get_device_state(self) -> dict[str, Any]:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/", timeout=timeout) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    async with session.get(
                        f"{base_url}/api/tlc/1/state/", timeout=timeout
                    ) as response2:
                        if response2.status == 200:
                            return await response2.json()
                        else:
                            _LOGGER.warning(f"Failed to get device state: {response.status}")
                            return {}
        except Exception as e:
            _LOGGER.error(f"Error getting device state: {e}")
            return {}


class OblamatikTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._current_temperature = state.get("temperature", 0.0)
        self.async_write_ha_state()


class OblamatikCurrentTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Current Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_current_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer-water"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._current_temperature = state.get("temperature", 0.0)
        self.async_write_ha_state()


class OblamatikFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water"
        self._attr_state_class = "measurement"
        self._current_flow = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_flow

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._current_flow = state.get("flow", 0.0)
        self.async_write_ha_state()


class OblamatikRequiredTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Required Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_required_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_state_class = "measurement"
        self._required_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._required_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._required_temperature = state.get("required_temp", 0.0)
        self.async_write_ha_state()


class OblamatikRequiredFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Required Flow ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_required_flow"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water-pump"
        self._attr_state_class = "measurement"
        self._required_flow = 0.0

    @property
    def native_value(self) -> float | None:
        return self._required_flow

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._required_flow = state.get("required_flow", 0.0)
        self.async_write_ha_state()


class OblamatikStatusSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Status ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_status"
        self._attr_icon = "mdi:information"
        self._current_status = "unknown"

    @property
    def native_value(self) -> str | None:
        return self._current_status

    async def async_update(self) -> None:
        state = await self._get_device_state()
        self._current_status = state.get("state", "unknown")
        self.async_write_ha_state()


class OblamatikWaterFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Water Flow State ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_water_flow_state"
        self._attr_icon = "mdi:water-pump"
        self._attr_state_class = None
        self._water_flow_state = "closed"

    @property
    def native_value(self) -> str | None:
        return self._water_flow_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        flow = state.get("flow", 0.0)
        self._water_flow_state = "open" if flow > 0 else "closed"
        self.async_write_ha_state()


class OblamatikBathFaucetSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Bath Faucet ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_faucet"
        self._attr_icon = "mdi:faucet"
        self._bath_faucet_state = "closed"

    @property
    def native_value(self) -> str | None:
        return self._bath_faucet_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        device_state = state.get("state", "unknown")
        self._bath_faucet_state = "open" if device_state == "a" else "closed"
        self.async_write_ha_state()


class OblamatikBathButtonSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Bath Button ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_button"
        self._attr_icon = "mdi:button-pointer"
        self._bath_button_state = False

    @property
    def native_value(self) -> bool | None:
        return self._bath_button_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        popup = state.get("popup", False)
        self._bath_button_state = bool(popup)
        self.async_write_ha_state()


class OblamatikFlowRateLiterPerHourSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate L/h ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow_rate_lh"
        self._attr_native_unit_of_measurement = "L/h"
        self._attr_icon = "mdi:water-speed"
        self._attr_state_class = "measurement"
        self._flow_rate_lh = 0.0

    @property
    def native_value(self) -> float | None:
        return self._flow_rate_lh

    async def async_update(self) -> None:
        state = await self._get_device_state()
        flow_lpm = state.get("flow", 0.0)
        self._flow_rate_lh = flow_lpm * 60
        self.async_write_ha_state()
