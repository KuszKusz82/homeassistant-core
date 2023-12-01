import logging
import time

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from .device_management_service import DeviceManagementService
from ..properties.thermal_actuator_properties import ThermalActuatorProperties
from ...common.enum.on_off_state import OnOffState

_LOGGER = logging.getLogger(__name__)


class CirculationService:
    def __init__(
            self,
            hass: HomeAssistant,
            service: DeviceManagementService,
            properties: ThermalActuatorProperties,
    ) -> None:
        self.__hass = hass
        self.__device_management_service = service
        self.__properties = properties

    def start_circulation(self) -> None:
        _LOGGER.info(f"Starting circulation. Properties: {self.__properties}")
        self.__update_desired_state(OnOffState.ON)
        self.__warmup()
        while self.__circulation_condition():
            self.__toggle()

        self.stop_circulation()

    def stop_circulation(self) -> None:
        _LOGGER.info(f"Stopping circulation. Properties: {self.__properties}")
        self.__update_desired_state(OnOffState.OFF)
        self.__turn_off()

    def __update_desired_state(self, state: OnOffState):
        self.__device_management_service.update_desired_state(
            self.__properties.ieee, state
        )

    def __circulation_condition(self) -> bool:
        return True

    def __warmup(self) -> None:
        self.__turn_on_and_sleep(self.__properties.warmup_seconds)
        self.__device_management_service.update_current_state(
            self.__properties.ieee, OnOffState.OFF
        )

    def __toggle(self) -> None:
        thermal_actuator = self.__device_management_service.read(self.__properties.ieee)
        if thermal_actuator.current_state == OnOffState.ON:
            self.__turn_off_and_sleep()
        else:
            self.__turn_on_and_sleep(self.__properties.intermediate_on_seconds)

    def __turn_on(self) -> bool:
        success = False
        try:
            _LOGGER.info(f"Switching on : {self.__properties.ieee}")
            service_data = {"entity_id": self.__properties.ieee}
            self.__hass.services.call("homeassistant", "turn_on", service_data, False)
            success = True
        except HomeAssistantError as Argument:
            _LOGGER.exception("Could not turn on actuator")
        return success

    def __turn_on_and_sleep(self, seconds: int) -> None:
        if self.__turn_on():
            time.sleep(seconds)
        else:
            time.sleep(self.__properties.intermediate_retry_seconds)

    def __turn_off(self) -> bool:
        success = False
        try:
            _LOGGER.info(f"Switching off : {self.__properties.ieee}")
            service_data = {"entity_id": self.__properties.ieee}
            self.__hass.services.call("homeassistant", "turn_off", service_data, False)
            success = True
        except HomeAssistantError as Argument:
            _LOGGER.exception("Could not turn off actuator")
        return success

    def __turn_off_and_sleep(self) -> None:
        if self.__turn_off():
            time.sleep(self.__properties.intermediate_off_seconds)
        else:
            time.sleep(self.__properties.intermediate_retry_seconds)
