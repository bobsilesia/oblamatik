"""Sensor platform for Oblamatik integration."""
import logging
from typing import Any, Dict, Optional

import aiohttp
from homeassistant.components.sensor import SensorEntity
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
    """Set up Oblamatik sensors."""
    _LOGGER.info("Setting up Oblamatik sensors")
    
    # Get devices from config entry
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating sensors for {len(devices)} devices")
    else:
        # Single device mode
        devices = [{
            "host": entry.data["host"],
            "port": entry.data.get("port", 80),
            "name": f"Oblamatik {entry.data['host']}"
        }]
    
    # Create sensor entities for each device
    sensors = []
    for device in devices:
        sensors.extend([
            OblamatikTemperatureSensor(hass, device),
            OblamatikFlowSensor(hass, device),
            OblamatikStatusSensor(hass, device),
            OblamatikWaterFlowSensor(hass, device),
            OblamatikCurrentTemperatureSensor(hass, device),
            OblamatikFlowRateLiterPerHourSensor(hass, device),
            OblomatikBathFaucetSensor(hass, device),
            OblomatikBathButtonSensor(hass, device),
        ])
    
    async_add_entities(sensors, True)


class OblamatikBaseSensor(SensorEntity):
    """Base class for Oblamatik sensors."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize sensor."""
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
            manufacturer="KWC/Viega",
            model="TLC15F/TLC30FTD",
        )
        self._attr_available = True

    async def _get_device_state(self) -> Dict[str, Any]:
        """Get current state from KWC/Viega device."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            # Try Viega API first
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_url}/api/tlc/1/", timeout=5) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        # Fallback to KWC API
                        async with session.get(f"{base_url}/api/tlc/1/state/", timeout=5) as response:
                            if response.status == 200:
                                return await response.json()
                            else:
                                _LOGGER.warning(f"Failed to get device state: {response.status}")
                                return {}
        except Exception as e:
            _LOGGER.error("Error getting device state: %s", e)
            return {}


class OblamatikTemperatureSensor(OblamatikBaseSensor):
    """Sensor for current temperature."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize temperature sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_temperature"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> Optional[float]:
        """Return the current temperature."""
        return self._current_temperature

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        self._current_temperature = state.get("temperature", 0.0)
        self.async_write_ha_state()


class OblamatikFlowSensor(OblamatikBaseSensor):
    """Sensor for current flow rate."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize flow sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_flow"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water"
        self._attr_state_class = "measurement"
        self._current_flow = 0.0

    @property
    def native_value(self) -> Optional[float]:
        """Return the current flow rate."""
        return self._current_flow

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        self._current_flow = state.get("flow", 0.0)
        self.async_write_ha_state()


class OblamatikStatusSensor(OblamatikBaseSensor):
    """Sensor for device status."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize status sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Status ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_status"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_status"
        self._attr_icon = "mdi:information"
        self._current_status = "unknown"

    @property
    def native_value(self) -> Optional[str]:
        """Return the current status."""
        return self._current_status

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        self._current_status = state.get("state", "unknown")
        self.async_write_ha_state()


class OblamatikWaterFlowSensor(OblamatikBaseSensor):
    """Sensor for water flow state (open/closed)."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize water flow sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Water Flow State ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_water_flow_state"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_water_flow_state"
        self._attr_icon = "mdi:water-pump"
        self._attr_state_class = None
        self._water_flow_state = "closed"

    @property
    def native_value(self) -> Optional[str]:
        """Return the water flow state."""
        return self._water_flow_state

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        flow = state.get("flow", 0.0)
        self._water_flow_state = "open" if flow > 0 else "closed"
        self.async_write_ha_state()


class OblamatikCurrentTemperatureSensor(OblamatikBaseSensor):
    """Sensor for current temperature (Viega compatible)."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize current temperature sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Current Temperature ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_current_temperature"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_current_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer-water"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> Optional[float]:
        """Return the current temperature."""
        return self._current_temperature

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        self._current_temperature = state.get("temperature", 0.0)
        self.async_write_ha_state()


class OblamatikFlowRateLiterPerHourSensor(OblamatikBaseSensor):
    """Sensor for flow rate in liters per hour."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize flow rate L/h sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Flow Rate L/h ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow_rate_lh"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_flow_rate_lh"
        self._attr_native_unit_of_measurement = "L/h"
        self._attr_icon = "mdi:water-speed"
        self._attr_state_class = "measurement"
        self._flow_rate_lh = 0.0

    @property
    def native_value(self) -> Optional[float]:
        """Return the current flow rate in L/h."""
        return self._flow_rate_lh

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        flow_lpm = state.get("flow", 0.0)  # L/min from API
        self._flow_rate_lh = flow_lpm * 60  # Convert to L/h
        self.async_write_ha_state()


class OblomatikBathFaucetSensor(OblamatikBaseSensor):
    """Sensor for bath faucet state (Viega)."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize bath faucet sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Bath Faucet ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_faucet"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_bath_faucet"
        self._attr_icon = "mdi:faucet"
        self._bath_faucet_state = "closed"

    @property
    def native_value(self) -> Optional[str]:
        """Return the bath faucet state."""
        return self._bath_faucet_state

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        device_state = state.get("state", "unknown")
        # Viega state 'a' might mean active/open
        self._bath_faucet_state = "open" if device_state == "a" else "closed"
        self.async_write_ha_state()


class OblomatikBathButtonSensor(OblamatikBaseSensor):
    """Sensor for bath button state (Viega)."""

    def __init__(self, hass: HomeAssistant, device: Dict[str, Any]) -> None:
        """Initialize bath button sensor."""
        super().__init__(hass, device)
        self._attr_name = f"Bath Button ({self._host})"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_button"
        self._attr_entity_id = f"sensor.oblamatik_{self._host.replace('.', '_')}_bath_button"
        self._attr_icon = "mdi:button-pointer"
        self._bath_button_state = False

    @property
    def native_value(self) -> Optional[bool]:
        """Return the bath button state."""
        return self._bath_button_state

    async def async_update(self) -> None:
        """Update sensor state."""
        state = await self._get_device_state()
        popup = state.get("popup", False)
        self._bath_button_state = bool(popup)
        self.async_write_ha_state()
