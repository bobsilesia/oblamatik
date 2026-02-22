"""Number platform for Oblamatik integration."""
import logging
from typing import Any, Dict, Optional

import aiohttp
from homeassistant.components.number import NumberEntity
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
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
    """Set up Oblamatik number entities."""
    _LOGGER.info("Setting up Oblamatik number entities")
    
    # Get devices from config entry
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating number entities for {len(devices)} devices")
    else:
        # Single device mode
        devices = [{
            "host": entry.data["host"],
            "port": entry.data.get("port", 80),
            "name": f"Oblamatik {entry.data['host']}"
        }]
    
    # Create number entities for each device
    numbers = []
    for device in devices:
        numbers.extend([
            OblamatikTemperatureNumber(hass, device),
            OblamatikFlowNumber(hass, device),
        ])
    
    async_add_entities(numbers, True)


class OblamatikBaseNumber(NumberEntity):
    """Base class for Oblamatik number entities."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize number entity."""
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
        self._attr_available = True

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


class OblamatikTemperatureNumber(OblamatikBaseNumber):
    """Number entity for precise temperature control."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize temperature number."""
        super().__init__(hass, device)
        self._attr_name = f"Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_temperature_number"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_native_min_value = 4.0
        self._attr_native_max_value = 80.0
        self._attr_native_step = 1.0
        self._attr_native_value = 38.0

    async def _get_current_flow(self) -> Optional[float]:
        """Get current flow from device."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{base_url}/api/state/", 
                    timeout=5
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Try to get flow from response
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
        """Set new temperature value."""
        _LOGGER.info(f"Setting temperature to {value}°C")
        self._attr_native_value = value
        
        # Get current flow to send with temperature command
        current_flow = await self._get_current_flow()
        if current_flow is None:
            current_flow = 0.0  # Fallback to default flow
            _LOGGER.warning(f"Could not get current flow, using fallback: {current_flow} L/min")
        
        # Send temperature command with current flow
        if await self._post_tlc(value, current_flow, True):
            _LOGGER.info(f"Temperature set successfully to {value}°C with flow {current_flow} L/min")
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set temperature")


class OblamatikFlowNumber(OblamatikBaseNumber):
    """Number entity for precise flow control."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize flow number."""
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow_number"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water"
        self._attr_native_min_value = 0.0
        self._attr_native_max_value = 10.0
        self._attr_native_step = 0.1
        self._attr_native_value = 0.0

    async def _get_current_temperature(self) -> Optional[float]:
        """Get current temperature from device."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{base_url}/api/state/", 
                    timeout=5
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Try to get temperature from response
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
        """Set new flow value."""
        _LOGGER.info(f"Setting flow rate to {value} L/min")
        self._attr_native_value = value
        
        # Get current temperature to send with flow command
        current_temp = await self._get_current_temperature()
        if current_temp is None:
            current_temp = 38.0  # Fallback to default temperature
            _LOGGER.warning(f"Could not get current temperature, using fallback: {current_temp}°C")
        
        # Send flow command with current temperature
        if await self._post_tlc(current_temp, value, True):
            _LOGGER.info(f"Flow rate set successfully to {value} L/min with temperature {current_temp}°C")
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set flow rate")
