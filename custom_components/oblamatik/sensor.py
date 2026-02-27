import logging
from typing import Any

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfInformation,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.info("Setting up Oblamatik sensors")
    if "devices" in entry.data:
        devices = entry.data["devices"]
        _LOGGER.info(f"Creating sensors for {len(devices)} devices")
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

    # Helper to check for valid temperature sensor
    async def _has_valid_temperature_sensor(host: str, port: int) -> bool:
        try:
            base_url = f"http://{host}:{port}"
            session = aiohttp_client.async_get_clientsession(hass)
            timeout = aiohttp.ClientTimeout(total=5)
            # Try primary endpoint
            try:
                async with session.get(f"{base_url}/api/tlc/1/", timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        temp = float(data.get("temperature", 0.0))
                        if temp > 99.0:
                            _LOGGER.warning(
                                "Device at %s reports invalid temperature (%.1f°C). "
                                "Temperature sensor will be disabled.",
                                host,
                                temp,
                            )
                            return False
                        return True
            except Exception:
                pass

            # Try fallback endpoint
            try:
                async with session.get(f"{base_url}/api/tlc/1/state/", timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        temp = float(data.get("temperature", 0.0))
                        if temp > 99.0:
                            _LOGGER.warning(
                                "Device at %s reports invalid temperature (%.1f°C). "
                                "Temperature sensor will be disabled.",
                                host,
                                temp,
                            )
                            return False
                        return True
            except Exception:
                pass

            return True  # Default to True if check fails to avoid disabling on temporary error
        except Exception as e:
            _LOGGER.warning(f"Failed to check temperature sensor for {host}: {e}")
            return True

    for device in devices:
        host = device["host"]
        port = device.get("port", 80)
        has_temp_sensor = await _has_valid_temperature_sensor(host, port)

        device_type = device.get("type", "unknown")

        # Common sensors for all types
        device_sensors = [
            OblamatikFlowSensor(hass, device),
            OblamatikStatusSensor(hass, device),
            OblamatikWaterFlowSensor(hass, device),
            OblamatikRequiredTemperatureSensor(hass, device),
            OblamatikUptimeSensor(hass, device),
            OblamatikSerialSensor(hass, device),
            OblamatikVersionSensor(hass, device),
            OblamatikFreeDiskSensor(hass, device),
            OblamatikFreeMemorySensor(hass, device),
            OblamatikWifiSsidSensor(hass, device),
            OblamatikMacAddressSensor(hass, device),
        ]

        if has_temp_sensor:
            device_sensors.append(OblamatikTemperatureSensor(hass, device))
            if device_type in ["bath", "shower"] or device_type not in ["kitchen"]:
                device_sensors.append(OblamatikCurrentTemperatureSensor(hass, device))

        if device_type in ["bath", "shower"] or device_type not in ["kitchen"]:
            device_sensors.extend(
                [
                    OblamatikRequiredFlowSensor(hass, device),
                    OblamatikBathFaucetSensor(hass, device),
                    OblamatikBathButtonSensor(hass, device),
                    OblamatikFlowRateLiterPerHourSensor(hass, device),
                ]
            )

        sensors.extend(device_sensors)

    async_add_entities(sensors, True)


class OblamatikBaseSensor(SensorEntity):
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
        )
        self._attr_has_entity_name = True
        self._attr_available = True

    async def _get_device_state(self) -> dict[str, Any]:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            try:
                async with session.get(f"{base_url}/api/tlc/1/", timeout=timeout) as response:
                    if response.status == 200:
                        return await response.json(content_type=None)
                    else:
                        async with session.get(
                            f"{base_url}/api/tlc/1/state/", timeout=timeout
                        ) as response2:
                            if response2.status == 200:
                                return await response2.json(content_type=None)
                            else:
                                _LOGGER.warning(f"Failed to get device state: {response.status}")
                                return {}
            except Exception as e:
                # Try fallback only if first attempt raised exception (not just bad status)
                try:
                    async with session.get(
                        f"{base_url}/api/tlc/1/state/", timeout=timeout
                    ) as response2:
                        if response2.status == 200:
                            return await response2.json(content_type=None)
                except Exception:
                    pass  # Ignore nested failure
                raise e  # Re-raise original error if fallback also failed

        except Exception as e:
            _LOGGER.error(f"Error getting device state for {self._host}: {e}")
            return {}


class OblamatikTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Temperature"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._current_temperature = float(state.get("temperature", 0.0))
        # Remove direct call to async_write_ha_state() as HA calls async_update automatically


class OblamatikCurrentTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Current Temperature"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_current_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer-water"
        self._attr_state_class = "measurement"
        self._current_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._current_temperature = float(state.get("temperature", 0.0))
        # Remove direct call to async_write_ha_state() as HA calls async_update automatically


class OblamatikFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Flow Rate"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:hydro-power"
        self._attr_state_class = "measurement"
        self._current_flow = 0.0

    @property
    def native_value(self) -> float | None:
        return self._current_flow

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._current_flow = float(state.get("flow", 0.0))


class OblamatikRequiredTemperatureSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Required Temperature"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_required_temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_state_class = "measurement"
        self._required_temperature = 0.0

    @property
    def native_value(self) -> float | None:
        return self._required_temperature

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._required_temperature = float(state.get("required_temp", 0.0))


class OblamatikRequiredFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Required Flow"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_required_flow"
        self._attr_native_unit_of_measurement = UnitOfVolumeFlowRate.LITERS_PER_MINUTE
        self._attr_icon = "mdi:water-pump"
        self._attr_state_class = "measurement"
        self._required_flow = 0.0

    @property
    def native_value(self) -> float | None:
        return self._required_flow

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._required_flow = float(state.get("required_flow", 0.0))


class OblamatikStatusSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Status"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_status"
        self._attr_icon = "mdi:information"
        self._current_status = "unknown"
        self._cancel_keep_alive = None

    @property
    def native_value(self) -> str | None:
        return self._current_status

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._cancel_keep_alive:
            self._cancel_keep_alive()
            self._cancel_keep_alive = None
        await super().async_will_remove_from_hass()

    @callback
    async def _force_update(self, *_: Any) -> None:
        """Force update of the entity."""
        self._cancel_keep_alive = None
        await self.async_update_ha_state(force_refresh=True)

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            raw_status = str(state.get("state", "unknown"))
            if raw_status == "a":
                self._current_status = "Idle"
            elif raw_status == "b":
                self._current_status = "Running"
            elif raw_status == "f":
                self._current_status = "Hygiene Active"
            else:
                self._current_status = raw_status

            # Keep-alive logic: ensure frequent updates while running
            # This is critical for Thermal Desinfection which may time out without polling
            if raw_status in ["b", "f"]:
                if self._cancel_keep_alive:
                    self._cancel_keep_alive()
                    self._cancel_keep_alive = None

                # Schedule next update in 2 seconds (safe keep-alive interval)
                self._cancel_keep_alive = async_call_later(self.hass, 2, self._force_update)



class OblamatikWaterFlowSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Water Flow"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_water_flow_state"
        self._attr_icon = "mdi:water-pump"
        self._attr_state_class = None
        self._water_flow_state = "closed"

    @property
    def native_value(self) -> str | None:
        return self._water_flow_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            flow = float(state.get("flow", 0.0))
            self._water_flow_state = "open" if flow > 0 else "closed"


class OblamatikBathFaucetSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Bath Faucet"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_faucet"
        self._attr_icon = "mdi:faucet"
        self._bath_faucet_state = "closed"

    @property
    def native_value(self) -> str | None:
        return self._bath_faucet_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            device_state = state.get("state", "unknown")
            self._bath_faucet_state = "open" if device_state == "a" else "closed"


class OblamatikBathButtonSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Bath Button"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_button"
        self._attr_icon = "mdi:button-pointer"
        self._bath_button_state = False

    @property
    def native_value(self) -> bool | None:
        return self._bath_button_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            popup = state.get("popup", False)
            self._bath_button_state = bool(popup)


class OblamatikFlowRateLiterPerHourSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Flow Rate L/h"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_flow_rate_lh"
        self._attr_native_unit_of_measurement = "L/h"
        self._attr_icon = "mdi:gauge-low"
        self._attr_state_class = "measurement"
        self._flow_rate_lh = 0.0

    @property
    def native_value(self) -> float | None:
        return self._flow_rate_lh

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            flow_lpm = float(state.get("flow", 0.0))
            self._flow_rate_lh = flow_lpm * 60


class OblamatikSystemBaseSensor(OblamatikBaseSensor):
    async def _get_device_state(self, required_key: str | None = None) -> dict[str, Any]:
        """Get system status from /api/ with fallback to base implementation.

        Args:
            required_key: Optional key that must be present in the response.
        """
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(f"{base_url}/api/", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    # If data is empty or missing key fields, trigger fallback
                    if data:
                        # If a specific key is required, check for it
                        if required_key and required_key not in data:
                            _LOGGER.debug(
                                f"Missing '{required_key}' in /api/ for {self._host}, fallback"
                            )
                            pass  # Fall through to fallback
                        elif "uptime" in data or "serial" in data or "version" in data:
                            return data
        except Exception as e:
            _LOGGER.debug(f"Error getting system state from /api/ for {self._host}: {e}")

        # Fallback to standard endpoint if /api/ fails or is incomplete
        _LOGGER.debug(f"System info fallback for {self._host}")
        return await super()._get_device_state()


class OblamatikUptimeSensor(OblamatikSystemBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Uptime"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_uptime"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:clock-outline"
        self._attr_entity_registry_enabled_default = False
        self._uptime_str = "00:00"

    @property
    def native_value(self) -> str | None:
        return self._uptime_str

    async def async_update(self) -> None:
        state = await self._get_device_state(required_key="uptime")
        uptime_seconds = 0
        if state:
            uptime_seconds = int(state.get("uptime", 0))

        # If uptime is 0, try fallback to base (skipping SystemBaseSensor logic)
        if uptime_seconds == 0:
            _LOGGER.debug(f"Uptime is 0 from /api/, trying fallback for {self._host}")
            # Call OblamatikBaseSensor._get_device_state directly
            state_fallback = await super(OblamatikSystemBaseSensor, self)._get_device_state()
            if state_fallback:
                uptime_seconds = int(state_fallback.get("uptime", 0))

        if uptime_seconds > 0:
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            self._uptime_str = f"{hours:02d}:{minutes:02d}"
        else:
            self._uptime_str = "00:00"


class OblamatikSerialSensor(OblamatikSystemBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Serial Number"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_serial"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:barcode"
        self._serial = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._serial

    async def async_update(self) -> None:
        state = await self._get_device_state(required_key="serial")
        if state:
            self._serial = str(state.get("serial", "Unknown"))


class OblamatikVersionSensor(OblamatikSystemBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Firmware Version"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_version"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:tag-text-outline"
        self._version = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._version

    async def async_update(self) -> None:
        state = await self._get_device_state(required_key="version")
        if state:
            self._version = str(state.get("version", "Unknown"))


class OblamatikFreeDiskSensor(OblamatikSystemBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Free Disk Space"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_free_disk"
        self._attr_native_unit_of_measurement = UnitOfInformation.KILOBYTES
        self._attr_device_class = "data_size"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:harddisk"
        self._attr_state_class = "measurement"
        self._attr_entity_registry_enabled_default = False
        self._free_disk = 0

    @property
    def native_value(self) -> int | None:
        return self._free_disk

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._free_disk = int(state.get("disk", 0))


class OblamatikFreeMemorySensor(OblamatikSystemBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Free Memory"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_free_memory"
        self._attr_native_unit_of_measurement = UnitOfInformation.KILOBYTES
        self._attr_device_class = "data_size"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:memory"
        self._attr_state_class = "measurement"
        self._attr_entity_registry_enabled_default = False
        self._free_memory = 0

    @property
    def native_value(self) -> int | None:
        return self._free_memory

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._free_memory = int(state.get("mem", 0))


class OblamatikWifiSsidSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Wi-Fi SSID"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_wifi_ssid"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:wifi"
        self._ssid = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._ssid

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            wlan = state.get("wlan") or {}
            self._ssid = str(wlan.get("name", "Unknown"))


class OblamatikMacAddressSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "MAC Address"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_mac_address"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:network"
        self._mac = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._mac

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            wlan = state.get("wlan") or {}
            self._mac = str(state.get("mac_address") or wlan.get("mac_address") or "Unknown")
