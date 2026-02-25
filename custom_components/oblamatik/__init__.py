import logging
from typing import Any

import aiohttp
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "oblamatik"

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.info("Setting up Oblamatik integration")
    return True


async def _get_device_info(hass: HomeAssistant, host: str, port: int) -> dict[str, Any] | None:
    session = aiohttp_client.async_get_clientsession(hass)
    timeout = aiohttp.ClientTimeout(total=5)

    # Try first endpoint
    try:
        url = f"http://{host}:{port}/api/tlc/1/"
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                try:
                    data = await response.json(content_type=None)
                    _LOGGER.info(f"Device {host} responded to primary endpoint with data: {data}")
                    return _process_device_data(data, host)
                except Exception as e:
                    _LOGGER.warning(
                        f"Device {host} responded 200 OK to primary endpoint "
                        f"but JSON decode failed: {e}"
                    )
                    text = await response.text()
                    _LOGGER.warning(f"Raw response: {text[:200]}...")  # Log first 200 chars
            else:
                _LOGGER.debug(
                    f"Device {host} returned status {response.status} on primary endpoint"
                )
    except Exception as e:
        _LOGGER.debug(f"Primary endpoint failed for {host}: {e}")

    # Try fallback endpoint
    try:
        url_state = f"http://{host}:{port}/api/tlc/1/state/"
        async with session.get(url_state, timeout=timeout) as response2:
            if response2.status == 200:
                try:
                    data2 = await response2.json(content_type=None)
                    _LOGGER.info(f"Device {host} responded to fallback endpoint with data: {data2}")
                    return _process_device_data(data2, host)
                except Exception as e:
                    _LOGGER.warning(
                        f"Device {host} responded 200 OK to fallback endpoint "
                        f"but JSON decode failed: {e}"
                    )
                    text = await response2.text()
                    _LOGGER.warning(f"Raw response: {text[:200]}...")
            else:
                _LOGGER.debug(
                    f"Device {host} returned status {response2.status} on fallback endpoint"
                )
    except Exception as e:
        _LOGGER.error(f"Fallback endpoint failed for {host}: {e}")

    return None


def _process_device_data(data: dict[str, Any], host: str) -> dict[str, Any]:
    device_type = _detect_device_type(data)
    name = data.get("name")
    if not name or name == f"Oblamatik {host}" or name == f"Oblamatik ({host})" or host in name:
        if device_type != "unknown":
            name = f"Oblamatik {device_type.title()}"
        else:
            name = f"Oblamatik {host}"

    return {
        "type": device_type,
        "model": data.get("model", "Unknown"),
        "name": name,
        "version": data.get("version", "Unknown"),
        "serial": data.get("serial", "Unknown"),
    }


def _detect_device_type(data: dict[str, Any]) -> str:
    device_type = data.get("type", "unknown")
    model = data.get("model", "").lower()
    type_mapping = {
        "1": "kitchen",
        "3": "shower",
        "4": "bath",
    }
    if "kitchen" in model:
        return "kitchen"
    elif "shower" in model:
        return "shower"
    elif "bath" in model:
        return "bath"
    elif device_type in type_mapping:
        return type_mapping[device_type]
    else:
        return "unknown"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Setting up Oblamatik entry")

    updated_devices = []
    entry_updated = False

    if "devices" in entry.data:
        # Create a deep copy of devices list to allow modification
        updated_devices = [dict(d) for d in entry.data["devices"]]
    else:
        # Handle legacy single-device config format
        updated_devices = [
            {
                "host": entry.data["host"],
                "port": entry.data.get("port", 80),
                "name": f"Oblamatik {entry.data['host']}",
                "type": "unknown",
                "model": "Unknown",
            }
        ]
        entry_updated = True

    # Check and update device info if missing or unknown, or if name contains IP
    for device in updated_devices:
        needs_update = (
            device.get("model") == "Unknown"
            or device.get("type") == "unknown"
            or "model" not in device
        )

        # Fix ugly names (containing IP) if type is known
        if not needs_update:
            current_name = device.get("name", "")
            # Check for various IP/Host patterns in name
            if (
                current_name == f"Oblamatik {device['host']}"
                or current_name == f"Oblamatik ({device['host']})"
                or device["host"] in current_name
            ):
                if device.get("type") and device.get("type") != "unknown":
                    device["name"] = f"Oblamatik {device['type'].title()}"
                    entry_updated = True
                    _LOGGER.info(f"Updated device name for {device['host']} to {device['name']}")

        if needs_update:
            _LOGGER.info(f"Attempting to update info for device {device['host']}")
            new_info = await _get_device_info(hass, device["host"], device.get("port", 80))
            if new_info and (new_info["model"] != "Unknown" or new_info["type"] != "unknown"):
                device.update(new_info)
                entry_updated = True
                _LOGGER.info(f"Updated device info for {device['host']}: {new_info}")

    if entry_updated:
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "devices": updated_devices}
        )

    _LOGGER.info(f"Setting up {len(updated_devices)} Oblamatik devices")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = updated_devices

    await hass.config_entries.async_forward_entry_setups(
        entry,
        [
            Platform.SWITCH,
            Platform.CLIMATE,
            Platform.SENSOR,
            Platform.NUMBER,
            Platform.BUTTON,
            Platform.BINARY_SENSOR,
        ],
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Unloading Oblamatik entry")
    return await hass.config_entries.async_unload_platforms(
        entry,
        [
            Platform.SWITCH,
            Platform.CLIMATE,
            Platform.SENSOR,
            Platform.NUMBER,
            Platform.BUTTON,
            Platform.BINARY_SENSOR,
        ],
    )
