from homeassistant.core import HomeAssistant
from ..properties.thermal_actuator_properties import ThermalActuatorProperties
from ..service.circulation_service import CirculationService
from ..service.device_management_service import DeviceManagementService


class ThermalActuatorConfig:
    def __init__(self, hass: HomeAssistant) -> None:
        self.__hass = hass
        self.__device_management_service = DeviceManagementService()

    def circulation_service(
            self, service_properties: ThermalActuatorProperties
    ) -> CirculationService:
        return CirculationService(
            self.__hass, self.__device_management_service, service_properties
        )
