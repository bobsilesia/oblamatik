"""Enhanced config flow with device type detection."""
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

    VERSION = 2

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, 80)
            
            # Test connection and detect device type
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
                        "devices": [{"host": host, "port": port, "name": device_info["name"], "type": device_info["type"], "model": device_info["model"]}]
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

    async def _test_connection_and_detect(self, host: str, port: int) -> Dict[str, Any]:
        """Test connection and detect device type."""
        import aiohttp
        try:
            url = f"http://{host}:{port}/api/tlc/1/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Detect device type based on response
                        device_type = self._detect_device_type(data)
                        
                        return {
                            "type": device_type,
                            "model": data.get("model", "Unknown"),
                            "name": data.get("name", f"Oblamatik {host}"),
                            "version": data.get("version", "Unknown"),
                            "serial": data.get("serial", "Unknown")
                        }
        except Exception as e:
            _LOGGER.error(f"Connection test failed: {e}")
            return None

    def _detect_device_type(self, data: Dict[str, Any]) -> str:
        """Detect device type based on API response."""
        device_type = data.get("type", "unknown")
        model = data.get("model", "").lower()
        
        # Map device types to human-readable names
        type_mapping = {
            "1": "kitchen",      # KWC TLC15F Kitchen
            "3": "shower",       # Viega TLC30FTD LCD Shower  
            "4": "bath",         # Viega TLC30FTD LCD Bath
        }
        
        # Enhanced detection based on model name
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
        """Create options flow for editing."""
        return config_entries.OptionsFlowHandler(config_entry)
