"""Support for controlling GPIO pins of a Raspberry Pi."""
import logging

from homeassistant.const import (
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "rpi_gpio"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.COVER,
    Platform.SWITCH,
]

_LOGGER = logging.getLogger(__name__)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Raspberry PI GPIO component."""

    def cleanup_gpio(event):
        """Stuff to do before stopping."""
        _LOGGER.info("GPIO.cleanup()")

    def prepare_gpio(event):
        """Stuff to do when Home Assistant starts."""
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup_gpio)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare_gpio)
    _LOGGER.info("GPIO.setmode(GPIO.BCM)")

    return True


def setup_output(port):
    """Set up a GPIO as output."""
    _LOGGER.info("GPIO.setup(%s, GPIO.OUT)", port)


def setup_input(port, pull_mode):
    """Set up a GPIO as input."""
    _LOGGER.info("GPIO.setup(%s, GPIO.IN, %s)", port, pull_mode)


def write_output(port, value):
    """Write a value to a GPIO."""
    _LOGGER.info("GPIO.output(%s, %s)", port, value)


def read_input(port):
    """Read a value from a GPIO."""
    _LOGGER.info("GPIO.input(%s)", port)
    return 1


def edge_detect(port, event_callback, bounce):
    """Add detection for RISING and FALLING events."""
    _LOGGER.info(
        "GPIO.add_event_detect(%s, GPIO.BOTH, %s, %s)", port, event_callback, bounce
    )
