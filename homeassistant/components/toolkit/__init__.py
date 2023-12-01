import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .shutter_driver import ShutterDriver
from .thermal_actuator import ThermalActuator

_LOGGER = logging.getLogger(__name__)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    ShutterDriver(hass)
    ThermalActuator(hass)

    # Return boolean to indicate that initialization was successful.
    return True
