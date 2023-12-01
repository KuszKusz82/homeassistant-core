import logging

from homeassistant.core import HomeAssistant, ServiceCall
from .config.shutter_driver_config import ShutterDriverConfig
from .properties.shutter_driver_properties import ShutterDriverProperties
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ShutterDriver:
    def __init__(self, hass: HomeAssistant) -> None:
        self.context = ShutterDriverConfig(hass)
        hass.services.register(
            DOMAIN, "execute_shutter_commands", self.execute_shutter_commands
        )

    def execute_shutter_commands(self, call: ServiceCall) -> None:
        _LOGGER.error(f"Handling:{call.data}")
        service_properties = ShutterDriverProperties(call.data)
        self.context.shutter_driver().execute_command(service_properties)
