import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACAction, HVACMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    _LOGGER.info("Setting up Oblamatik climate entities")
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating climate entities for {len(devices)} devices")
    else:
        devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
            }
        ]
    climates = [OblamatikClimate(hass, device) for device in devices]
    async_add_entities(climates, True)


class OblamatikClimate(ClimateEntity):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__()
        self._hass = hass
        self._device = device
        self._host = device["host"]
        self._port = device.get("port", 80)
        self._attr_name = "Temp Control"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_climate"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=device.get("name", f"Oblamatik ({self._host})"),
            manufacturer="KWC",
            model="TLC15F",
        )
        self._attr_has_entity_name = True
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_max_temp = 80.0
        self._attr_min_temp = 4.0
        self._attr_target_temperature = 38.0
        self._attr_current_temperature = 20.0
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_hvac_action = HVACAction.IDLE
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def available(self) -> bool:
        return True

    async def async_set_temperature(self, **kwargs: Any) -> None:
        temperature = kwargs.get("temperature")
        if temperature is None:
            return
        _LOGGER.info(f"Setting temperature to {temperature}°C")
        self._attr_target_temperature = temperature
        if await self._post_tlc(temperature, 0.0, True):
            _LOGGER.info(f"Temperature set successfully to {temperature}°C")
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set temperature")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        _LOGGER.info(f"Setting HVAC mode to {hvac_mode}")
        self._attr_hvac_mode = hvac_mode
        if hvac_mode == HVACMode.HEAT:
            if await self._post_tlc(self._attr_target_temperature, 0.0, True):
                _LOGGER.info("Heating turned on")
                self._attr_hvac_action = HVACAction.HEATING
            else:
                _LOGGER.error("Failed to turn on heating")
        else:
            if await self._post_tlc(15.0, 0.0, False):
                _LOGGER.info("Heating turned off")
                self._attr_hvac_action = HVACAction.IDLE
            else:
                _LOGGER.error("Failed to turn off heating")
        self.async_write_ha_state()

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
