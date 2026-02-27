import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
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
                OblamatikEmergencyStopButton(hass, device),
                OblamatikQuickAction1Button(hass, device),
                OblamatikQuickAction2Button(hass, device),
                OblamatikQuickAction3Button(hass, device),
                OblamatikOpenDrainButton(hass, device),
                OblamatikCloseDrainButton(hass, device),
                OblamatikWlanRestartButton(hass, device),
                OblamatikFunctionTestStep1Button(hass, device),
                OblamatikFunctionTestStep2Button(hass, device),
                OblamatikFunctionTestStep3Button(hass, device),
                OblamatikRebootButton(hass, device),
                OblamatikHygieneStartButton(hass, device),
                OblamatikHygieneCancelButton(hass, device),
            ]
        )

    async_add_entities(buttons)


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
                    self._start_fast_status_refresh()
                    return True
                _LOGGER.warning(f"Command failed: {response.status}")
                return False
        except Exception as e:
            _LOGGER.error(f"Error sending command: {e}")
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


class OblamatikEmergencyStopButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Emergency Stop"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_stop"
        self._attr_icon = "mdi:alert-octagon"

    async def _get_current_target_temp(self) -> float | None:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/tlc/1/state/", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    if "required_temp" in data:
                        return float(data["required_temp"])
        except Exception as e:
            _LOGGER.warning(f"Failed to get current target temp: {e}")
        return None

    async def async_press(self) -> None:
        target_temp = await self._get_current_target_temp()
        if target_temp is None:
            target_temp = 10.0  # Fallback

        # Stop water flow immediately
        await self._post_command("/api/tlc/1/", f"temperature={target_temp}&flow=0&changed=1")
        # Ensure hygiene mode is cancelled if active
        await self._post_command("/api/tlc/1/hygiene/thermal-desinfection/cancel/", "data=1")


class OblamatikQuickAction1Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Quick Action 1"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_quick_1"
        self._attr_icon = "mdi:numeric-1-box"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/quick/1/", "data=1")


class OblamatikQuickAction2Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Quick Action 2"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_quick_2"
        self._attr_icon = "mdi:numeric-2-box"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/quick/2/", "data=1")


class OblamatikQuickAction3Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Quick Action 3"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_quick_3"
        self._attr_icon = "mdi:numeric-3-box"

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/quick/3/", "data=1")


class OblamatikWlanRestartButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "WLAN (AP mode)"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_wlan_restart"
        self._attr_icon = "mdi:wifi-refresh"
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        # Calls wlan/disconnect/ to reset to AP mode (effectively restarting WLAN)
        await self._post_command("/api/wlan/disconnect/", "")


class OblamatikFunctionTestStep1Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Function Test Step 1"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_func_test_1"
        self._attr_icon = "mdi:test-tube"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/functional-test/step/1/", "")


class OblamatikFunctionTestStep2Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Function Test Step 2"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_func_test_2"
        self._attr_icon = "mdi:test-tube"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/functional-test/step/2/", "")


class OblamatikFunctionTestStep3Button(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Function Test Step 3"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_func_test_3"
        self._attr_icon = "mdi:test-tube"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/functional-test/step/3/", "")


class OblamatikRebootButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Reboot Device"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_reboot"
        self._attr_icon = "mdi:restart"
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/functional-test/step/0/", "0=1")


class OblamatikHygieneStartButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Hygiene Start"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_hygiene_start"
        self._attr_icon = "mdi:bacteria-outline"
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        # tlc_service.js: startDesinfection(TLCid) -> POST .../start/ [TLCid]
        # In JS: $rootScope.request(..., [TLCid], TLCid)
        # The data payload is an array with the ID: [1]
        # Need to check if aiohttp handles list as data correctly if passing string "1" or JSON.
        # PHP: $command = explode('/', $_GET['url']); ...
        # But wait, tlc-hygiene.php checks $_POST.
        # JS request function probably JSON encodes body?
        # Let's assume sending "1" or JSON `[1]`.
        # tlc_service.js:
        # return $rootScope.request("tlc/" + TLCid + "/hygiene/thermal-desinfection/start/",
        #                           "POST", [TLCid], TLCid);
        # So payload is `[1]`.
        # PHP `do_desinfect`: $out = print_r($_POST, true); ...
        # If it expects JSON body, PHP `$_POST` might be empty
        # unless Content-Type is application/x-www-form-urlencoded and key=val.
        # Angular $http usually sends JSON.
        # PHP `file_get_contents('php://input')` is needed for raw JSON.
        # But the existing `_post_command` sends `application/x-www-form-urlencoded`.
        # Let's check `tlc-hygiene.php` again.
        # It calls `do_desinfect($command[4], $command[1])`.
        # It doesn't use `$_POST` data for `start` command logic, only logs it.
        # `set_desinfect()` is called.
        # So the payload might not matter for `start`.
        await self._post_command("/api/tlc/1/hygiene/thermal-desinfection/start/", "data=1")


class OblamatikHygieneCancelButton(OblamatikBaseButton):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Hygiene Stop"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_hygiene_cancel"
        self._attr_icon = "mdi:stop-circle-outline"
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        await self._post_command("/api/tlc/1/hygiene/thermal-desinfection/cancel/", "data=1")


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
