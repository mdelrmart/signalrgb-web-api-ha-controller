import logging
import voluptuous as vol
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_RGB_COLOR, LightEntity, PLATFORM_SCHEMA, SUPPORT_COLOR
)
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

# Definir configuración en configuration.yaml
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT, default=8080): cv.port,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    
    api = SignalRGBAPI(host, port, username, password)
    
    # Definir efectos disponibles
    effects = [
        {"name": "Color Cycle", "properties": {}},
        {"name": "Solid Color", "properties": {"color": "color"}}
    ]
    
    add_entities([RGBLight(api, effect) for effect in effects])

class RGBLight(LightEntity):
    def __init__(self, api, effect):
        self._api = api
        self._name = effect["name"]
        self._properties = effect["properties"]
        self._state = False
        self._color = (255, 255, 255)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_COLOR if "color" in self._properties else 0

    def turn_on(self, **kwargs):
        params = {}
        if ATTR_RGB_COLOR in kwargs and "color" in self._properties:
            params["color"] = "%02x%02x%02x" % kwargs[ATTR_RGB_COLOR]
        if self._api.set_effect(self._name, **params):
            self._state = True
            self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        self._state = False
        self.schedule_update_ha_state()
