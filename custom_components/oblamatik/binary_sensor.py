import logging
from typing import Any

import aiohttp
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.info("Setting up Oblamatik binary sensors")
    if "devices" in entry.data:
        devices = entry.data["devices"]
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
        sensors.append(OblamatikPopupBinarySensor(hass, device))

    async_add_entities(sensors, True)


class OblamatikBaseBinarySensor(BinarySensorEntity):
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
            configuration_url=f"http://{self._host}:{self._port}/",
        )
        self._attr_has_entity_name = True
        self._attr_available = True


class OblamatikPopupBinarySensor(OblamatikBaseBinarySensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Drain Position"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_popup"
        self._attr_device_class = BinarySensorDeviceClass.OPENING
        self._attr_icon = "mdi:valve"

    async def async_update(self) -> None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/popup/", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    # PHP: echo(json_encode(array('state' => $state)));
                    # Assuming 1 = open (Plug UP), 0 = closed (Plug DOWN).
                    state = data.get("state")
                    if state is not None:
                        self._attr_is_on = int(state) == 1
                        self._attr_available = True
                    else:
                        self._attr_available = False
                else:
                    self._attr_available = False
        except Exception as e:
            _LOGGER.debug(f"Error getting popup state for {self._host}: {e}")
            self._attr_available = False
