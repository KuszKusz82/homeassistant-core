from typing import Optional

from ..model.thermal_actuator import ThermalActuator


class ThermalActuatorRepository:
    thermal_actuators = dict[str, ThermalActuator]()

    @classmethod
    def exists(cls, identifier: str) -> bool:
        return identifier in cls.thermal_actuators

    @classmethod
    def find_by_id(cls, identifier: str) -> Optional[ThermalActuator]:
        return cls.thermal_actuators.get(identifier)

    @classmethod
    def save(cls, entity: ThermalActuator):
        cls.thermal_actuators[entity.ieee] = entity
