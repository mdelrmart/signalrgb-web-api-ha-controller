import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN  

_LOGGER = logging.getLogger(__name__)

class SignalRGBAPIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flujo de configuración para Mi API RGB."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Primer paso de configuración."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("port", default=8080): int,
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }),
            )
        return self.async_create_entry(title="SignalRGB Web API Home Assistant Controller", data=user_input)
