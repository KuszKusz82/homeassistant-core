import unittest
import logging
import time
import asyncio
from typing import Any

from unittest.mock import patch, MagicMock
from homeassistant.core import HomeAssistant, ServiceCall, Context, ServiceResponse

from homeassistant.components.toolkit.shutter_driver import ShutterDriver

_LOGGER = logging.getLogger(__name__)


class ShutterDriverIT(unittest.TestCase):
    @patch("homeassistant.core.HomeAssistant")
    @patch("homeassistant.core.ServiceCall")
    def test(self, hass: HomeAssistant, call: ServiceCall):
        ShutterDriver.setup(hass)

        call.data = {
            "lock_group": "livingroom",
            "devices": ["1", "2", "3", "4", "5"],
            "command": "UP",
        }

        hass.services.call = slowFn
        loop = asyncio.get_event_loop()
        tasks = list()
        for i in range(5):
            tasks.append(loop.create_task(ShutterDriver.execute_shutter_commands(call)))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


def slowFn(
    self,
    domain: str,
    service: str,
    service_data: dict[str, Any] | None = None,
    blocking: bool = False,
    context: Context | None = None,
    target: dict[str, Any] | None = None,
    return_response: bool = False,
) -> ServiceResponse:
    time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s %(levelname)s %(message)s"
    )
    unittest.main()
