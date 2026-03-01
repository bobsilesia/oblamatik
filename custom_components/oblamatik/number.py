import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfVolumeFlowRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers import entity_registry as er
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
                OblamatikMeasuringCupAmountNumber(hass, device),
                OblamatikHygieneIntervalNumber(hass, device),
                OblamatikHygieneFlushDurationNumber(hass, device),
                OblamatikFillAmountNumber(hass, device),
                OblamatikFillTemperatureNumber(hass, device),
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
            configuration_url=f"http://{self._host}:{self._port}/",
        )
        self._attr_has_entity_name = True
        self._attr_available = True

    async def _post_tlc(self, temperature: float, flow: float, changed_type: int) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = f"temperature={temperature}&flow={flow}&changed={changed_type}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/tlc/1/", data=data, headers=headers, timeout=timeout
            ) as response:
                success = response.status == 200
                if success:
                    _LOGGER.info(
                        f"Sent TLC command: temp={temperature}, flow={flow}, changed={changed_type}"
                    )
                    self._start_fast_status_refresh()
                else:
                    _LOGGER.warning(f"TLC command failed: {response.status}")
                return success
        except Exception as e:
            _LOGGER.error("Error sending TLC command: %s", e)
            return False

    def _start_fast_status_refresh(self) -> None:
        runtime = self._hass.data.setdefault(DOMAIN, {}).setdefault("runtime", {})
        tasks: dict[str, Any] = runtime.setdefault("fast_status_refresh_tasks", {})
        key = f"{self._host}:{self._port}"
        existing = tasks.get(key)
        if existing is not None and not existing.done():
            return
        tasks[key] = self._hass.async_create_task(self._async_fast_status_refresh())

    async def _async_fast_status_refresh(self) -> None:
        registry = er.async_get(self._hass)
        status_unique_id = f"{DOMAIN}_{self._host}_status"
        entity_id = er.async_get_entity_id(registry, "sensor", DOMAIN, status_unique_id)
        if not entity_id:
            return
        for _ in range(10):
            await self._hass.services.async_call(
                "homeassistant",
                "update_entity",
                {"entity_id": entity_id},
                blocking=False,
            )
            await asyncio.sleep(1)


class OblamatikTemperatureNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Temperature"
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
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/state/", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    if "required_flow" in data:
                        return float(data["required_flow"])
                    elif "flow" in data:
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
        if await self._post_tlc(value, current_flow, 1):
            _LOGGER.info(
                f"Temperature set successfully to {value}°C with flow {current_flow} L/min"
            )
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set temperature")


class OblamatikFlowNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Flow Rate"
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
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/state/", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    if "required_temp" in data:
                        return float(data["required_temp"])
                    elif "temperature" in data:
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
            _LOGGER.warning(f"Could not get current temp, using fallback: {current_temp}°C")
        if await self._post_tlc(current_temp, value, 2):
            _LOGGER.info(f"Flow rate set successfully to {value} L/min with temp {current_temp}°C")
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set flow rate")


class OblamatikMeasuringCupAmountNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Measuring Cup Amount"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_measuring_cup_amount"
        self._attr_native_unit_of_measurement = "L"
        self._attr_icon = "mdi:cup-water"
        self._attr_native_min_value = 0.1
        self._attr_native_max_value = 25.0
        self._attr_native_step = 0.1
        self._attr_native_value = 0.5

    async def async_update(self) -> None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(
                f"{base_url}/api/index.php?url=tlc-measuring-cup/1/get/", timeout=timeout
            ) as response:
                if response.status != 200:
                    return
                data = await response.json(content_type=None)
        except Exception as e:
            _LOGGER.debug("Error getting measuring cup amount for %s: %s", self._host, e)
            return

        if isinstance(data, dict):
            try:
                amount = float(data.get("amount", self._attr_native_value or 0.5))
                if amount > 0:
                    self._attr_native_value = amount
            except (TypeError, ValueError):
                return

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = f"amount={value}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/index.php?url=tlc-measuring-cup/1/save/",
                data=data,
                headers=headers,
                timeout=timeout,
            ) as response:
                if response.status == 200:
                    _LOGGER.info("Saved measuring cup amount %.1f L for %s", value, self._host)
                else:
                    _LOGGER.warning(
                        "Failed to save measuring cup amount for %s: %s",
                        self._host,
                        response.status,
                    )
        except Exception as e:
            _LOGGER.error("Error saving measuring cup amount for %s: %s", self._host, e)


class OblamatikHygieneIntervalNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Hygiene Interval"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_hygiene_interval"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_native_min_value = 0.0
        self._attr_native_max_value = 30.0
        self._attr_native_step = 0.5
        self._attr_native_value = 0.0

    async def _get_hygiene_state(self) -> dict[str, Any] | None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(
                f"{base_url}/api/index.php?url=tlc-hygiene/1/", timeout=timeout
            ) as response:
                if response.status != 200:
                    return None
                return await response.json(content_type=None)
        except Exception as e:
            _LOGGER.debug("Error getting hygiene state for %s: %s", self._host, e)
            return None

    async def _post_hygiene(
        self, repetition_period: float, flush_duration: float, active: bool
    ) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            active_str = "true" if active else "false"
            data = (
                f"repetition_period={repetition_period}"
                f"&flush_duration={flush_duration}"
                f"&hygiene_flush_active={active_str}"
            )
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/index.php?url=tlc-hygiene/1/",
                data=data,
                headers=headers,
                timeout=timeout,
            ) as response:
                if response.status == 200:
                    _LOGGER.info(
                        "Updated hygiene config on %s: interval=%s days, duration=%s s, active=%s",
                        self._host,
                        repetition_period,
                        flush_duration,
                        active,
                    )
                    return True
                _LOGGER.warning(
                    "Failed to update hygiene config for %s: %s", self._host, response.status
                )
                return False
        except Exception as e:
            _LOGGER.error("Error updating hygiene config for %s: %s", self._host, e)
            return False

    async def async_update(self) -> None:
        state = await self._get_hygiene_state()
        if not isinstance(state, dict):
            return
        try:
            value = float(state.get("repetition_period", self._attr_native_value or 0.0))
            if value >= 0:
                self._attr_native_value = value
        except (TypeError, ValueError):
            return

    async def async_set_native_value(self, value: float) -> None:
        state = await self._get_hygiene_state()
        if not isinstance(state, dict):
            return
        try:
            flush_duration = float(state.get("flush_duration", 60))
        except (TypeError, ValueError):
            flush_duration = 60.0
        active = bool(state.get("hygiene_flush_active", False))
        if await self._post_hygiene(value, flush_duration, active):
            self._attr_native_value = value
            self.async_write_ha_state()


class OblamatikHygieneFlushDurationNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Hygiene Flush Duration"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_hygiene_flush_duration"
        self._attr_icon = "mdi:timer-outline"
        self._attr_native_min_value = 10.0
        self._attr_native_max_value = 900.0
        self._attr_native_step = 10.0
        self._attr_native_value = 60.0

    async def _get_hygiene_state(self) -> dict[str, Any] | None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(
                f"{base_url}/api/index.php?url=tlc-hygiene/1/", timeout=timeout
            ) as response:
                if response.status != 200:
                    return None
                return await response.json(content_type=None)
        except Exception as e:
            _LOGGER.debug("Error getting hygiene state for %s: %s", self._host, e)
            return None

    async def _post_hygiene(
        self, repetition_period: float, flush_duration: float, active: bool
    ) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            active_str = "true" if active else "false"
            data = (
                f"repetition_period={repetition_period}"
                f"&flush_duration={flush_duration}"
                f"&hygiene_flush_active={active_str}"
            )
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/index.php?url=tlc-hygiene/1/",
                data=data,
                headers=headers,
                timeout=timeout,
            ) as response:
                if response.status == 200:
                    _LOGGER.info(
                        "Updated hygiene config on %s: interval=%s days, duration=%s s, active=%s",
                        self._host,
                        repetition_period,
                        flush_duration,
                        active,
                    )
                    return True
                _LOGGER.warning(
                    "Failed to update hygiene config for %s: %s", self._host, response.status
                )
                return False
        except Exception as e:
            _LOGGER.error("Error updating hygiene config for %s: %s", self._host, e)
            return False

    async def async_update(self) -> None:
        state = await self._get_hygiene_state()
        if not isinstance(state, dict):
            return
        try:
            value = float(state.get("flush_duration", self._attr_native_value or 60.0))
            if value > 0:
                self._attr_native_value = value
        except (TypeError, ValueError):
            return

    async def async_set_native_value(self, value: float) -> None:
        state = await self._get_hygiene_state()
        if not isinstance(state, dict):
            return
        try:
            repetition_period = float(state.get("repetition_period", 0.0))
        except (TypeError, ValueError):
            repetition_period = 0.0
        active = bool(state.get("hygiene_flush_active", False))
        if await self._post_hygiene(repetition_period, value, active):
            self._attr_native_value = value
            self.async_write_ha_state()


class OblamatikFillAmountNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Fill Amount"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_fill_amount"
        self._attr_native_unit_of_measurement = "L"
        self._attr_icon = "mdi:beaker-outline"
        self._attr_native_min_value = 10.0
        self._attr_native_max_value = 300.0
        self._attr_native_step = 1.0
        self._attr_native_value = 50.0

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()


class OblamatikFillTemperatureNumber(OblamatikBaseNumber):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Fill Temperature"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_fill_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer-water"
        self._attr_native_min_value = 10.0
        self._attr_native_max_value = 60.0
        self._attr_native_step = 0.5
        self._attr_native_value = 38.0

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()
