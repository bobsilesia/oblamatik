import logging
from typing import Any

import aiohttp
from homeassistant.components.button import ButtonEntity
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
    _LOGGER.info("Setting up Oblamatik buttons")
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

    buttons = []
    for device in devices:
        buttons.extend(
            [
                OblamatikStopButton(hass, device),
                OblamatikQuickAction1Button(hass, device),
                OblamatikOpenDrainButton(hass, device),
                OblamatikCloseDrainButton(hass, device),
            ]
        )

    async_add_entities(buttons, True)


class OblamatikBaseButton(ButtonEntity):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__()
        self._hass = hass
        self._device = device
        self._host = device["host"]
        self._port = device.get("port", 80)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=device.get("name", f"Oblamatik ({self._host})"),
            manufacturer="KWC/Viega/Crosswater",
            model=device.get("model", "Unknown"),
        )
        self._attr_has_entity_name = True
        self._attr_available = True

    async def _post_command(self, endpoint: str, data: str) -> bool:
        try:
            base_url = f"http://{self._host}:{self._port}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.post(
                f"{base_url}{endpoint}", data=data, headers=headers, timeout=timeout
            ) as response:
                if response.status == 200:
                    return True
                _LOGGER.warning(f"Command failed: {response.status}")
                return False
        except Exception as e:
            _LOGGER.error(f"Error sending command: {e}")
            return False


class OblamatikStopButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Stop"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_stop"
        self._attr_icon = "mdi:stop"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/", "temperature=10&flow=0&changed=1")


class OblamatikQuickAction1Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Quick Action 1"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_quick_1"
        self._attr_icon = "mdi:numeric-1-box"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/quick/1/", "data=1")


class OblamatikOpenDrainButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Open Drain"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_open_drain"
        self._attr_icon = "mdi:valve-open"

    async def async_press(self) -> None:
        # Assuming endpoint based on 'popup' state field and typical API structure
        await self._post_command("/api/tlc/1/popup/", "data=1")


class OblamatikCloseDrainButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Close Drain"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_close_drain"
        self._attr_icon = "mdi:valve-closed"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/popup/", "data=0")
