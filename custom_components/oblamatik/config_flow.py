"""Config flow for Oblamatik integration."""
import logging
from typing import Any, Dict, List, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)

DOMAIN = "oblamatik"


class OblamatikConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oblamatik."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, 80)
            
            # Test connection
            if await self._test_connection(host, port):
                return self.async_create_entry(
                    title=f"Oblamatik ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_PORT: port,
                        "devices": [{"host": host, "port": port, "name": f"Oblamatik {host}"}]
                    }
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="192.168.1.172"): str,
                vol.Optional(CONF_PORT, default=80): int,
            }),
            errors=errors
        )

    async def _test_connection(self, host: str, port: int) -> bool:
        """Test if we can connect to Oblamatik device."""
        import aiohttp
        try:
            url = f"http://{host}:{port}/api/tlc/1/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    return response.status == 200
        except Exception:
            return False

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create options flow for editing."""
        return config_entries.OptionsFlowHandler(config_entry)
