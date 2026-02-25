import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import aiohttp_client

_LOGGER = logging.getLogger(__name__)
DOMAIN = "oblamatik"


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow):
    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle the initial step."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["manual", "scan"],
        )

    async def async_step_manual(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle manual configuration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, 80)
            device_info = await self._test_connection_and_detect(host, port)
            if device_info:
                return self.async_create_entry(
                    title=f"Oblamatik ({device_info['name']})",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        "device_type": device_info["type"],
                        "model": device_info["model"],
                        "name": device_info["name"],
                        "devices": [
                            {
                                "host": host,
                                "port": port,
                                "name": device_info["name"],
                                "type": device_info["type"],
                                "model": device_info["model"],
                            }
                        ],
                    },
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=80): int,
                }
            ),
            errors=errors,
        )

    async def async_step_scan(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle automatic scanning."""
        # Simple scan logic: check if any devices were discovered via DHCP/Zeroconf
        # Since active scanning is complex and requires privileges, we rely on HA discovery
        # If no devices found, we inform user to use manual or check network

        return self.async_show_form(
            step_id="scan",
            errors={"base": "no_devices_found"},
            description_placeholders={
                "link": "https://github.com/bobsilesia/oblamatik/wiki/Installation"
            },
        )

    async def async_step_dhcp(self, discovery_info: Any) -> Any:
        """Handle DHCP discovery."""
        host = discovery_info.ip
        # Check if already configured
        await self.async_set_unique_id(discovery_info.macaddress)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        # Test connection
        device_info = await self._test_connection_and_detect(host, 80)
        if not device_info:
            return self.async_abort(reason="cannot_connect")

        device_info["host"] = host  # Ensure host is present
        self._discovered_device = device_info

        self.context["title_placeholders"] = {"name": device_info["name"]}
        return await self.async_step_confirm_discovery(None)

    async def async_step_zeroconf(self, discovery_info: Any) -> Any:
        """Handle Zeroconf discovery."""
        host = discovery_info.host
        # Zeroconf host might be oblamatik.local.
        if host.endswith("."):
            host = host[:-1]

        # Test connection
        device_info = await self._test_connection_and_detect(host, 80)
        if not device_info:
            return self.async_abort(reason="cannot_connect")

        device_info["host"] = host  # Ensure host is present
        self._discovered_device = device_info

        # Use serial or MAC if available in device_info as unique_id, else fallback
        if device_info.get("serial") and device_info["serial"] != "Unknown":
            await self.async_set_unique_id(device_info["serial"])
            self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        self.context["title_placeholders"] = {"name": device_info["name"]}
        return await self.async_step_confirm_discovery(None)

    async def async_step_confirm_discovery(self, user_input: dict[str, Any] | None = None) -> Any:
        """Confirm discovery."""
        if user_input is not None:
            # Retrieve host from context updates or re-detect?
            # DHCP sets updates={CONF_HOST: host} in _abort_if_unique_id_configured if matched,
            # but here we are in a new flow.
            # We need to find where we stored the host.
            # In async_step_dhcp, we called _test_connection_and_detect, but didn't store
            # the result for creation.
            # Let's fix async_step_dhcp and zeroconf to store data in self.context

            # Actually, we should store it in self._discovered_device
            if not hasattr(self, "_discovered_device") or not self._discovered_device:
                return self.async_abort(reason="no_device_info")

            device_info = self._discovered_device
            host = device_info["host"]  # We need to ensure host is in device_info
            port = 80  # Default

            return self.async_create_entry(
                title=self.context.get("title_placeholders", {}).get("name", "Oblamatik"),
                data={
                    CONF_HOST: host,
                    CONF_PORT: port,
                    "device_type": device_info["type"],
                    "model": device_info["model"],
                    "name": device_info["name"],
                    "devices": [
                        {
                            "host": host,
                            "port": port,
                            "name": device_info["name"],
                            "type": device_info["type"],
                            "model": device_info["model"],
                        }
                    ],
                },
            )

        return self.async_show_form(
            step_id="confirm_discovery",
            description_placeholders=self.context.get("title_placeholders", {}),
        )

    async def _test_connection_and_detect(self, host: str, port: int) -> dict[str, Any] | None:
        session = aiohttp_client.async_get_clientsession(self.hass)
        timeout = aiohttp.ClientTimeout(total=5)

        # Try first endpoint
        try:
            url = f"http://{host}:{port}/api/tlc/1/"
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    device_type = self._detect_device_type(data)
                    return {
                        "type": device_type,
                        "model": data.get("model", "Unknown"),
                        "name": self._get_clean_name(data, host, device_type),
                        "version": data.get("version", "Unknown"),
                        "serial": data.get("serial", "Unknown"),
                    }
        except Exception as e:
            _LOGGER.debug(f"Primary endpoint failed: {e}")

        # Try fallback endpoint
        try:
            url_state = f"http://{host}:{port}/api/tlc/1/state/"
            async with session.get(url_state, timeout=timeout) as response2:
                if response2.status == 200:
                    data2 = await response2.json(content_type=None)
                    device_type = self._detect_device_type(data2)
                    return {
                        "type": device_type,
                        "model": data2.get("model", "Unknown"),
                        "name": self._get_clean_name(data2, host, device_type),
                        "version": data2.get("version", "Unknown"),
                        "serial": data2.get("serial", "Unknown"),
                    }
        except Exception as e:
            _LOGGER.error(f"Fallback endpoint failed: {e}")

        return None

    def _get_clean_name(self, data: dict[str, Any], host: str, device_type: str) -> str:
        name = data.get("name")
        if not name or name == f"Oblamatik {host}" or name == f"Oblamatik ({host})" or host in name:
            if device_type != "unknown":
                return f"Oblamatik {device_type.title()}"
            return f"Oblamatik {host}"
        return name

    def _detect_device_type(self, data: dict[str, Any]) -> str:
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

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return OblamatikOptionsFlow(config_entry)


class OblamatikOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> Any:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_HOST,
                        default=self._entry.options.get(
                            CONF_HOST, self._entry.data.get(CONF_HOST, "")
                        ),
                    ): str,
                    vol.Optional(
                        CONF_PORT,
                        default=self._entry.options.get(
                            CONF_PORT, self._entry.data.get(CONF_PORT, 80)
                        ),
                    ): int,
                }
            ),
        )
