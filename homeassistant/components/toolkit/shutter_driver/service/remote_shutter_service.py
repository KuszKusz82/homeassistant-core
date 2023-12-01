import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class RemoteShutterService:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    def execute_command(self, command: str) -> None:
        _LOGGER.info("Calling remote service: {}".format(command))
        data = {
            "entity_id": "remote.broadlink_remote",
            "device": "Redőny",
            "command": command,
        }
        self.hass.services.call("remote", "send_command", data, True)
