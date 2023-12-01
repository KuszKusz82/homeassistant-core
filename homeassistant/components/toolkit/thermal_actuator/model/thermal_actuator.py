from ...common.enum.on_off_state import OnOffState


class ThermalActuator:
    def __init__(self, ieee: str) -> None:
        self.__ieee: str = ieee
        self.__current_state = OnOffState.OFF
        self.__desired_state = OnOffState.OFF

    @property
    def ieee(self):
        return self.__ieee

    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, value):
        self.__current_state = value

    @property
    def desired_state(self):
        return self.__desired_state

    @desired_state.setter
    def desired_state(self, value):
        self.__desired_state = value
