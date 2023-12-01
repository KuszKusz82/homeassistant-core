import logging

from .lock_service import LockService
from .remote_shutter_service import RemoteShutterService
from ..properties.shutter_driver_properties import ShutterDriverProperties

_LOGGER = logging.getLogger(__name__)


class ShutterServiceGuard:
    def __init__(
            self, lock_service: LockService, shutter_service: RemoteShutterService
    ) -> None:
        self.lock_service = lock_service
        self.shutter_service = shutter_service

    def execute_command(self, properties: ShutterDriverProperties) -> None:
        lock_group = properties.lock_group
        key = self.lock_service.ensure_group_lock(lock_group)
        try:
            if self.lock_service.acquire_lock(lock_group, key):
                for device in properties.devices:
                    self.try_execute_single_command(
                        device + "_" + properties.command, lock_group, key
                    )

            else:
                self.lock_service.steal_lock(lock_group, key)
                for device in properties.devices:
                    self.try_execute_single_command(
                        device + "_" + "STOP", lock_group, key
                    )
        finally:
            self.lock_service.release_lock(lock_group, key)

    def try_execute_single_command(self, device_command, lock_group: str, key: int):
        if self.lock_service.is_lock_acquired(lock_group, key):
            self.shutter_service.execute_command(device_command)
        else:
            _LOGGER.info(
                "Not executing command: {}. Service call cancelled. Lock not acquired".format(
                    device_command
                )
            )
