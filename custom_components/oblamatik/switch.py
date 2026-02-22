"""Switch platform for Oblamatik integration."""
import logging
from typing import Any, Dict, Optional
import asyncio

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Oblamatik switches."""
    _LOGGER.info("Setting up Oblamatik switches")
    
    # Get devices from config entry
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating switches for {len(devices)} devices")
    else:
        # Single device mode
        devices = [{
            "host": entry.data["host"],
            "port": entry.data.get("port", 80),
            "name": f"Oblamatik {entry.data['host']}"
        }]
    
    # Create switch entities for each device
    switches = []
    for device in devices:
        switches.extend([
            OblamatikWaterSwitch(hass, device),
            OblamatikHeatingSwitch(hass, device),
        ])
    
    async_add_entities(switches, True)


class OblamatikBaseSwitch(SwitchEntity):
    """Base class for Oblamatik switches."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize switch."""
        super().__init__()
        self._hass = hass
        self._device = device
        self._host = device["host"]
        self._port = device.get("port", 80)
        self._attr_name = None  # Will be set by subclasses
        self._attr_unique_id = None  # Will be set by subclasses
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=device.get("name", f"Oblamatik ({self._host})"),
            manufacturer="KWC",
            model="TLC15F",
        )
        self._is_on = False
        self._current_temperature = 38.0
        self._current_flow = 0.0

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    async def _get_device_state(self) -> Dict[str, Any]:
        """Get current state from KWC device."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_url}/api/tlc/1/state/", timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        _LOGGER.warning(f"Failed to get KWC state: {response.status}")
                        return {}
        except Exception as e:
            _LOGGER.error("Error getting KWC state: %s", e)
            return {}

    async def _post_quick(self) -> bool:
        """Activate quick mode."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = "data=1"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/api/tlc/1/quick/1/", 
                    data=data, 
                    headers=headers, 
                    timeout=5
                ) as response:
                    success = response.status == 200
                    if success:
                        _LOGGER.info("Successfully activated quick mode")
                    else:
                        _LOGGER.warning(f"Quick mode failed: {response.status}")
                    return success
        except Exception as e:
            _LOGGER.error("Error activating quick mode: %s", e)
            return False

    async def _post_tlc(self, temperature: float, flow: float, changed: bool) -> bool:
        """Send TLC command."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            data = f"temperature={temperature}&flow={flow}&changed={1 if changed else 0}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/api/tlc/1/", 
                    data=data, 
                    headers=headers, 
                    timeout=5
                ) as response:
                    success = response.status == 200
                    if success:
                        _LOGGER.info(f"Successfully sent TLC command: temp={temperature}, flow={flow}")
                    else:
                        _LOGGER.warning(f"TLC command failed: {response.status}")
                    return success
        except Exception as e:
            _LOGGER.error("Error sending TLC command: %s", e)
            return False

    async def _monitor_state(self, stop_condition: str = "a") -> bool:
        """Monitor device state until condition is met."""
        try:
            for _ in range(30):  # Monitor for 30 seconds
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
    """Switch for controlling water flow."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize water switch."""
        super().__init__(hass, device)
        self._attr_name = f"Water Flow ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_water_flow"
        self._attr_icon = "mdi:water"

    @property
    def is_on(self) -> bool:
        """Return True if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on water switch."""
        _LOGGER.info("Turning on water flow")
        
        # 1. Activate quick mode
        if not await self._post_quick():
            _LOGGER.error("Failed to activate quick mode")
            return
        
        # 2. Set temperature and flow
        if not await self._post_tlc(self._current_temperature, 0.5, True):
            _LOGGER.error("Failed to set water flow")
            return
        
        # 3. Monitor state
        await self._monitor_state("a")
        
        self._is_on = True
        self._current_flow = 0.5
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off water switch."""
        _LOGGER.info("Turning off water flow")
        
        # 1. Send stop command
        if not await self._post_tlc(self._current_temperature, 0.0, False):
            _LOGGER.error("Failed to send stop command")
            return
        
        # 2. Wait a moment for command to process
        await asyncio.sleep(1)
        
        # 3. Verify state change
        state = await self._get_device_state()
        if state.get("flow", 0) == 0:
            _LOGGER.info("Water flow successfully stopped")
            self._is_on = False
            self._current_flow = 0.0
            self.async_write_ha_state()
        else:
            _LOGGER.warning(f"Water still flowing after stop command. State: {state}")
            # Try alternative method - force stop
            await self._post_quick()
            await asyncio.sleep(0.5)
            await self._post_tlc(self._current_temperature, 0.0, False)
            await asyncio.sleep(1)
            
            # Final verification
            final_state = await self._get_device_state()
            if final_state.get("flow", 0) == 0:
                self._is_on = False
                self._current_flow = 0.0
                self.async_write_ha_state()
                _LOGGER.info("Water flow stopped with alternative method")
            else:
                _LOGGER.error(f"Failed to stop water flow. Final state: {final_state}")


class OblamatikHeatingSwitch(OblamatikBaseSwitch):
    """Switch for controlling heating."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize heating switch."""
        super().__init__(hass, device)
        self._attr_name = f"Heating ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_heating"
        self._attr_icon = "mdi:thermometer"

    @property
    def is_on(self) -> bool:
        """Return True if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on heating."""
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
        """Turn off heating."""
        _LOGGER.info("Turning off heating")
        
        if await self._post_tlc(15.0, 0.0, False):
            self._is_on = False
            self._current_temperature = 15.0
            self.async_write_ha_state()
            _LOGGER.info("Heating turned off successfully")
        else:
            _LOGGER.error("Failed to turn off heating")
