import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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
    _LOGGER.info("Setting up Oblamatik switches")
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating switches for {len(devices)} devices")
    else:
        devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
            }
        ]
    switches = []
    for device in devices:
        switches.extend(
            [
                OblamatikWaterSwitch(hass, device),
                OblamatikHeatingSwitch(hass, device),
            ]
        )
    async_add_entities(switches, True)


class OblamatikBaseSwitch(SwitchEntity):
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
        self._attr_has_entity_name = True
        self._is_on = False
        self._current_temperature = 38.0
        self._current_flow = 0.0

    @property
    def available(self) -> bool:
        return True

    async def _get_device_state(self) -> dict[str, Any]:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/state/", timeout=timeout) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.warning(f"Failed to get KWC state: {response.status}")
                    return {}
        except Exception as e:
            _LOGGER.error("Error getting KWC state: %s", e)
            return {}

    async def _post_quick(self) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = "data=1"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/tlc/1/quick/1/", data=data, headers=headers, timeout=timeout
            ) as response:
                success = response.status == 200
                if success:
                    _LOGGER.info("Successfully activated quick mode")
                    self._start_fast_status_refresh()
                else:
                    _LOGGER.warning(f"Quick mode failed: {response.status}")
                return success
        except Exception as e:
            _LOGGER.error("Error activating quick mode: %s", e)
            return False

    async def _post_tlc(self, temperature: float, flow: float, changed: bool) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = f"temperature={temperature}&flow={flow}&changed={1 if changed else 0}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}/api/tlc/1/", data=data, headers=headers, timeout=timeout
            ) as response:
                success = response.status == 200
                if success:
                    _LOGGER.info(f"Successfully sent TLC command: temp={temperature}, flow={flow}")
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
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, status_unique_id)
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

    async def _monitor_state(self, stop_condition: str = "a") -> bool:
        try:
            for _ in range(30):
                state = await self._get_device_state()
                if state.get("state") == stop_condition:
                    _LOGGER.info(f"State reached: {stop_condition}")
                    return True
                await asyncio.sleep(1)
            _LOGGER.warning(f"Timeout waiting for state: {stop_condition}")
            return False
        except Exception as e:
            _LOGGER.error("Error monitoring state: %s", e)
            return False


class OblamatikWaterSwitch(OblamatikBaseSwitch):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Water Flow"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_water_flow"
        self._attr_icon = "mdi:water"

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        _LOGGER.info("Turning on water flow")
        if not await self._post_quick():
            _LOGGER.error("Failed to activate quick mode")
            return
        if not await self._post_tlc(self._current_temperature, 0.5, True):
            _LOGGER.error("Failed to set water flow")
            return
        await self._monitor_state("a")
        self._is_on = True
        self._current_flow = 0.5
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.info("Turning off water flow")
        if not await self._post_tlc(self._current_temperature, 0.0, False):
            _LOGGER.error("Failed to send stop command")
            return
        await asyncio.sleep(1)
        state = await self._get_device_state()
        if state.get("flow", 0) == 0:
            _LOGGER.info("Water flow successfully stopped")
            self._is_on = False
            self._current_flow = 0.0
            self.async_write_ha_state()
        else:
            _LOGGER.warning(f"Water still flowing after stop command. State: {state}")
            await self._post_quick()
            await asyncio.sleep(0.5)
            await self._post_tlc(self._current_temperature, 0.0, False)
            await asyncio.sleep(1)
            final_state = await self._get_device_state()
            if final_state.get("flow", 0) == 0:
                self._is_on = False
                self._current_flow = 0.0
                self.async_write_ha_state()
                _LOGGER.info("Water flow stopped with alternative method")
            else:
                _LOGGER.error(f"Failed to stop water flow. Final state: {final_state}")


class OblamatikHeatingSwitch(OblamatikBaseSwitch):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Heating"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_heating_switch"
        self._attr_icon = "mdi:fire"

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        temp = kwargs.get("temperature", 40)
        _LOGGER.info(f"Turning on heating to {temp}°C")
        if await self._post_tlc(temp, 0.0, True):
            self._is_on = True
            self._current_temperature = temp
            self.async_write_ha_state()
            _LOGGER.info(f"Heating turned on successfully to {temp}°C")
        else:
            _LOGGER.error("Failed to turn on heating")

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.info("Turning off heating")
        if await self._post_tlc(15.0, 0.0, False):
            self._is_on = False
            self._current_temperature = 15.0
            self.async_write_ha_state()
            _LOGGER.info("Heating turned off successfully")
        else:
            _LOGGER.error("Failed to turn off heating")
