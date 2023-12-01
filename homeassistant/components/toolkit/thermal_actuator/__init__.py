import asyncio
import logging

from homeassistant.core import HomeAssistant, ServiceCall
from .config.thermal_actuator_config import ThermalActuatorConfig
from .properties.thermal_actuator_properties import ThermalActuatorProperties
from .repository.thermal_actuator_repository import ThermalActuatorRepository
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_REPOSITORY = ThermalActuatorRepository


class ThermalActuator:
    def __init__(self, hass: HomeAssistant) -> None:
        self.context = ThermalActuatorConfig(hass)
        hass.services.register(
            DOMAIN, "thermal_actuator_start_circulation", self.start_circulation
        )
        hass.services.register(
            DOMAIN, "thermal_actuator_stop_circulation", self.stop_circulation
        )

    def start_circulation(self, call: ServiceCall) -> None:
        asyncio.run(self.do_start_circulation(call))

    def stop_circulation(self, call: ServiceCall) -> None:
        asyncio.run(self.do_stop_circulation(call))

    async def do_stop_circulation(self, call: ServiceCall):
        service_properties = ThermalActuatorProperties(call.data)
        self.context.circulation_service(service_properties).stop_circulation()

    async def do_start_circulation(self, call: ServiceCall):
        service_properties = ThermalActuatorProperties(call.data)
        self.context.circulation_service(service_properties).start_circulation()
