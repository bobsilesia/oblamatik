import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "oblamatik"

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.info("Setting up Oblamatik integration")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Setting up Oblamatik entry")

    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Setting up {len(devices)} Oblamatik devices")
    else:
        devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
            }
        ]

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = devices

    await hass.config_entries.async_forward_entry_setups(
        entry,
        [
            Platform.SWITCH,
            Platform.CLIMATE,
            Platform.SENSOR,
            Platform.NUMBER,
            Platform.BUTTON,
        ],
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Unloading Oblamatik entry")
    return await hass.config_entries.async_unload_platforms(
        entry,
        [Platform.SWITCH, Platform.CLIMATE, Platform.SENSOR, Platform.NUMBER, Platform.BUTTON],
    )
