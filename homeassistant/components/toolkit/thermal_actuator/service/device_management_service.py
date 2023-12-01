import threading

from ..model.thermal_actuator import ThermalActuator
from ..properties import thermal_actuator_properties
from ..repository.thermal_actuator_repository import ThermalActuatorRepository
from ...common.enum.on_off_state import OnOffState


class DeviceManagementService:
    repository = ThermalActuatorRepository
    repository_lock = threading.RLock()

    @classmethod
    def read(cls, identifier: str) -> ThermalActuator:
        thermal_actuator = cls.repository.find_by_id(identifier)
        if thermal_actuator is None:
            raise ValueError("Optional value is None")
        return thermal_actuator

    @classmethod
    def ensure_exists(cls, properties: thermal_actuator_properties.ThermalActuatorProperties) -> None:
        with cls.repository_lock:
            thermal_actuator = cls.repository.find_by_id(properties.ieee)
            if thermal_actuator is None:
                thermal_actuator = ThermalActuator(properties.ieee)
                cls.repository.save(thermal_actuator)

    @classmethod
    def update_current_state(cls, identifier: str, state: OnOffState):
        repository = cls.repository

        thermal_actuator = repository.find_by_id(identifier)
        if thermal_actuator is not None:
            thermal_actuator.current_state = state

    @classmethod
    def update_desired_state(cls, identifier: str, state: OnOffState):
        repository = cls.repository

        thermal_actuator = repository.find_by_id(identifier)
        if thermal_actuator is not None:
            thermal_actuator.current_state = state
