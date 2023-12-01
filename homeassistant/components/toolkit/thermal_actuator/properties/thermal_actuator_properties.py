import logging
from typing import Any

from ...common.util.any_util import as_int

_LOGGER = logging.getLogger(__name__)


class ThermalActuatorProperties:
    def __init__(self, data: dict[str, Any]) -> None:
        _LOGGER.info(f"Parsing data: {data}")
        self._ieee = str(data.get("ieee"))
        self._warmup_seconds = as_int(data.get("warmup_seconds"))
        self._intermediate_off_seconds = as_int(data.get("intermediate_off_seconds"))
        self._intermediate_on_seconds = as_int(data.get("intermediate_on_seconds"))
        self._intermediate_retry_seconds = as_int(data.get("intermediate_retry_seconds"))

    @property
    def ieee(self):
        return self._ieee

    @property
    def warmup_seconds(self):
        return self._warmup_seconds

    @property
    def intermediate_off_seconds(self):
        return self._intermediate_off_seconds

    @property
    def intermediate_on_seconds(self):
        return self._intermediate_on_seconds

    @property
    def intermediate_retry_seconds(self):
        return self._intermediate_retry_seconds
