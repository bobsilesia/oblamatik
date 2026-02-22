"""Oblamatik Integration for Home Assistant."""
import logging
from typing import Any, Dict, Optional

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "oblamatik"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Oblamatik integration."""
    _LOGGER.info("Setting up Oblamatik integration")
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up Oblamatik from a config entry."""
    _LOGGER.info("Setting up Oblamatik entry")
    
    # Get devices from config entry
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Setting up {len(devices)} Oblamatik devices")
    else:
        # Single device mode
        devices = [{
            "host": entry.data["host"],
            "port": entry.data.get("port", 80),
            "name": f"Oblamatik {entry.data['host']}"
        }]
    
    # Store devices for platforms
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = devices
    
    # Forward setup to all platforms
    await hass.config_entries.async_forward_entry_setups(entry, [
        Platform.SWITCH,
        Platform.CLIMATE,
        Platform.SENSOR,
        Platform.NUMBER,
    ])
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Oblamatik entry")
    
    # Forward unload to all platforms
    return await hass.config_entries.async_forward_entry_unload(entry, [
        Platform.SWITCH, Platform.CLIMATE, Platform.SENSOR, Platform.NUMBER
    ])
from .websocket import OblamatikWebSocket, OblamatikRealTimeUpdater
