from homeassistant.core import HomeAssistant
from ..service.lock_service import LockService
from ..service.remote_shutter_service import RemoteShutterService
from ..service.shutter_service_guard import ShutterServiceGuard


class ShutterDriverConfig:
    def __init__(self, hass: HomeAssistant) -> None:
        self.__lock_service = LockService()
        self.__remote_shutter_service = RemoteShutterService(hass)

    def shutter_driver(self) -> ShutterServiceGuard:
        return ShutterServiceGuard(self.__lock_service, self.__remote_shutter_service)
