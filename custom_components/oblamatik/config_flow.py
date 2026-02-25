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
                return self.async_create_entry(
                    title=f"Oblamatik ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        "device_type": "unknown",
                        "model": "Unknown",
                        "name": f"Oblamatik {host}",
                        "devices": [
                            {
                                "host": host,
                                "port": port,
                                "name": f"Oblamatik {host}",
                                "type": "unknown",
                                "model": "Unknown",
                            }
                        ],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default="192.168.1.172"): str,
                    vol.Optional(CONF_PORT, default=80): int,
                }
            ),
            errors=errors,
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
