import logging
import aiohttp
from homeassistant.components.light import (
    ATTR_RGB_COLOR, LightEntity, COLOR_MODE_RGB
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Configura la integración de luces a partir de una entrada de configuración."""
    api = SignalRGBAPI(
        entry.data["host"],
        entry.data["port"],
        entry.data["username"],
        entry.data["password"],
    )
    
    # Definir efectos disponibles
    effects = [
        {"name": "Color Cycle", "properties": {}},
        {"name": "Solid Color", "properties": {"color": "color"}}
    ]
    
    async_add_entities([RGBLight(api, effect) for effect in effects])

class RGBLight(LightEntity):
    """Clase que representa una luz RGB controlada por la API."""

    def __init__(self, api, effect):
        """Inicializa la luz con el efecto especificado."""
        self._api = api
        self._attr_name = effect["name"]
        self._properties = effect["properties"]
        self._attr_is_on = False
        self._attr_color_mode = COLOR_MODE_RGB if "color" in self._properties else None
        self._attr_supported_color_modes = {COLOR_MODE_RGB} if "color" in self._properties else set()
        self._attr_rgb_color = (255, 255, 255)

    async def async_turn_on(self, **kwargs):
        """Enciende la luz con el efecto actual."""
        params = {}
        if ATTR_RGB_COLOR in kwargs and "color" in self._properties:
            params["color"] = "%02x%02x%02x" % kwargs[ATTR_RGB_COLOR]
        
        if await self._api.set_effect(self._attr_name, **params):
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Apaga la luz."""
        self._attr_is_on = False
        self.async_write_ha_state()
