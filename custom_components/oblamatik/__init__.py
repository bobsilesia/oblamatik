"""The Oblamatik integration."""
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the Oblamatik component."""
    _LOGGER.info("Setting up Oblamatik integration")
    return True
