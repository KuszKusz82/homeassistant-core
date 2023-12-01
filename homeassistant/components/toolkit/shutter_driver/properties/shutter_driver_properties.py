import logging
from typing import Any

from ...common.util.any_util import as_list, as_str

_LOGGER = logging.getLogger(__name__)


class ShutterDriverProperties:
    def __init__(self, data: dict[str, Any]) -> None:
        _LOGGER.info(f"Parsing data: {data}")
        self._lock_group = as_str(data.get("lock_group"))
        self._devices = as_list(data.get("devices"))
        self._command = as_str(data.get("command"))

    @property
    def lock_group(self):
        return self._lock_group

    @property
    def devices(self):
        return self._devices

    @property
    def command(self):
        return self._command
