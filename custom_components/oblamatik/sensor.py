import logging
import random
from typing import Any

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
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
            OblamatikDeviceSerialSensor(hass, device),
            OblamatikDeviceVersionSensor(hass, device),
            OblamatikWifiSsidSensor(hass, device),
            OblamatikMacAddressSensor(hass, device),
            OblamatikNetworkModeSensor(hass, device),
            OblamatikIPAddressSensor(hass, device),
            OblamatikIoTSerialSensor(hass, device),
            OblamatikIoTVersionSensor(hass, device),
            OblamatikSignalStrengthSensor(hass, device),
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
                    OblamatikBathDrainSensor(hass, device),
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
            manufacturer="KWC",
            model=device.get("model", "Unknown"),
            configuration_url=f"http://{self._host}:{self._port}/",
        )
        self._attr_has_entity_name = True
        self._attr_available = True

    async def _get_device_state(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            try:
                async with session.get(
                    f"{base_url}/api/tlc/1/", params=params, timeout=timeout
                ) as response:
                    if response.status == 200:
                        return await response.json(content_type=None)
                    else:
                        async with session.get(
                            f"{base_url}/api/tlc/1/state/", params=params, timeout=timeout
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
                        f"{base_url}/api/tlc/1/state/", params=params, timeout=timeout
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
        # Use random query parameter to prevent caching and ensure Keep-Alive works
        # This mimics the behavior of the original app which sends ?q=...
        params = {"q": str(random.random())}
        state = await self._get_device_state(params=params)
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

                # Schedule next update in 1 second (aggressive heartbeat)
                self._cancel_keep_alive = async_call_later(self.hass, 1, self._force_update)


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


class OblamatikBathDrainSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Bath Drain"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_bath_drain"
        self._attr_icon = "mdi:valve"
        self._bath_drain_state = False

    @property
    def native_value(self) -> bool | None:
        return self._bath_drain_state

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            popup = state.get("popup", False)
            self._bath_drain_state = bool(popup)


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


class OblamatikIoTSensorBase(OblamatikBaseSensor):
    async def _get_device_state(
        self, params: dict[str, Any] | None = None, required_key: str | None = None
    ) -> dict[str, Any]:
        """Get IoT system status from /api/info (mapped to info.php)."""
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=5)
            # Use /api/info which corresponds to info.php in firmware
            async with session.get(
                f"{base_url}/api/info", params=params, timeout=timeout
            ) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    if data:
                        return data
        except Exception as e:
            _LOGGER.debug(f"Error getting IoT info from /api/info for {self._host}: {e}")
            # Try fallback to /api/ (some firmwares might differ)
            try:
                async with session.get(
                    f"{base_url}/api/", params=params, timeout=timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        if data:
                            return data
            except Exception:
                pass

        return {}


class OblamatikDeviceSerialSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Device Serial Number"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_serial"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:barcode"
        self._serial = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._serial

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._serial = str(state.get("serial", "Unknown"))


class OblamatikDeviceVersionSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Device Firmware Version"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_version"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:tag-text-outline"
        self._version = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._version

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._version = str(state.get("version", "Unknown"))


class OblamatikIoTSerialSensor(OblamatikIoTSensorBase):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "IoT Serial Number"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_iot_serial"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:barcode-scan"
        self._serial = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._serial

    async def async_update(self) -> None:
        # Try getting from /api/info first
        state = await self._get_device_state(required_key="serial_number_iot")
        serial = state.get("serial_number_iot")

        # If not found, try getting from /api/tlc/1/ (fallback 1)
        if not serial:
            try:
                base_url = f"http://{self._host}:{self._port}"
                session = aiohttp_client.async_get_clientsession(self._hass)
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(f"{base_url}/api/tlc/1/", timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        serial = data.get("serial_number_iot")
            except Exception:
                pass

        # If still not found, try getting from /inc/info.txt (fallback 2)
        if not serial:
            try:
                base_url = f"http://{self._host}:{self._port}"
                session = aiohttp_client.async_get_clientsession(self._hass)
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(f"{base_url}/inc/info.txt", timeout=timeout) as response:
                    if response.status == 200:
                        # info.txt content: {"version":"...","serial_number_iot":"..."}
                        # It might be JSON or text. Based on file content, it is JSON.
                        try:
                            data = await response.json(content_type=None)
                            serial = data.get("serial_number_iot")
                        except Exception:
                            # Try parsing as text if JSON fails
                            text = await response.text()
                            import json

                            data = json.loads(text)
                            serial = data.get("serial_number_iot")
            except Exception:
                pass

        if serial:
            self._serial = str(serial)


class OblamatikIoTVersionSensor(OblamatikIoTSensorBase):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "IoT Firmware Version"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_iot_version"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:chip"
        self._version = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._version

    async def async_update(self) -> None:
        state = await self._get_device_state(required_key="version")
        if state:
            self._version = str(state.get("version", "Unknown"))


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


class OblamatikNetworkModeSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Network Mode"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_network_mode"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:access-point-network"
        self._network_mode = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._network_mode

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            raw_mode = str(state.get("network", "Unknown"))
            if raw_mode == "wlan_ap":
                self._network_mode = "Access Point"
                self._attr_icon = "mdi:access-point-network"
            elif raw_mode == "wlan_cl":
                self._network_mode = "Client (WiFi)"
                self._attr_icon = "mdi:wifi"
            elif raw_mode == "ethernet":
                self._network_mode = "Client (Ethernet)"
                self._attr_icon = "mdi:ethernet"
            elif raw_mode == "br-lan":
                self._network_mode = "Client (Bridged)"
                self._attr_icon = "mdi:lan-connect"
            else:
                self._network_mode = raw_mode
                self._attr_icon = "mdi:help-network"


class OblamatikIPAddressSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "IP Address"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_ip_address"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:ip-network"
        self._ip = "Unknown"

    @property
    def native_value(self) -> str | None:
        return self._ip

    async def async_update(self) -> None:
        state = await self._get_device_state()
        if state:
            self._ip = str(state.get("ip", "Unknown"))


class OblamatikSignalStrengthSensor(OblamatikBaseSensor):
    def __init__(self, hass: HomeAssistant, device: dict[str, Any]) -> None:
        super().__init__(hass, device)
        self._attr_name = "Wi-Fi Signal Strength"
        self._attr_unique_id = f"{DOMAIN}_{self._host}_signal_strength"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:wifi-strength-2"
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = "measurement"
        # Disable by default as it requires scanning which might be slow
        self._attr_entity_registry_enabled_default = False
        self._signal_strength = 0

    @property
    def native_value(self) -> int | None:
        return self._signal_strength

    async def async_update(self) -> None:
        # First get current SSID from device state
        state = await self._get_device_state()
        if not state:
            return

        wlan = state.get("wlan") or {}
        current_ssid = str(wlan.get("name", ""))

        if not current_ssid or current_ssid == "Unknown":
            return

        # Now scan for networks to get signal strength
        try:
            base_url = f"http://{self._host}:{self._port}"
            session = aiohttp_client.async_get_clientsession(self._hass)
            timeout = aiohttp.ClientTimeout(total=10)  # Scan takes time
            async with session.get(f"{base_url}/api/wlan/", timeout=timeout) as response:
                if response.status == 200:
                    networks = await response.json(content_type=None)

                    if isinstance(networks, dict):
                        networks = list(networks.values())

                    for network in networks:
                        if isinstance(network, dict) and network.get("name") == current_ssid:
                            raw_signal = float(network.get("rawsignal", 0))
                            # Convert raw signal (0-70 or similar) to percentage
                            # Assuming 70 is max quality
                            self._signal_strength = int(min(100, max(0, (raw_signal / 70) * 100)))
                            break
        except Exception as e:
            _LOGGER.debug(f"Error scanning wifi for {self._host}: {e}")
