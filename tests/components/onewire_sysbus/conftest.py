"""Provide common 1-Wire fixtures."""
from unittest.mock import MagicMock, patch

import pytest

from homeassistant.components.onewire_sysbus.const import (
    CONF_MOUNT_DIR,
    DEFAULT_SYSBUS_MOUNT_DIR,
    DOMAIN,
)
from homeassistant.config_entries import SOURCE_USER, ConfigEntry
from homeassistant.core import HomeAssistant

from .const import MOCK_SYSBUS_DEVICES

from tests.common import MockConfigEntry


@pytest.fixture(name="device_id", params=MOCK_SYSBUS_DEVICES.keys())
def get_device_id(request: pytest.FixtureRequest) -> str:
    """Parametrize device id."""
    return request.param


@pytest.fixture(name="config_entry")
def get_config_entry(hass: HomeAssistant) -> ConfigEntry:
    """Create and register mock config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_MOUNT_DIR: DEFAULT_SYSBUS_MOUNT_DIR,
        },
        unique_id=DEFAULT_SYSBUS_MOUNT_DIR,
        entry_id="3",
    )
    config_entry.add_to_hass(hass)
    return config_entry


@pytest.fixture(name="sysbus")
def get_sysbus() -> MagicMock:
    """Mock sysbus."""
    with patch(
        "homeassistant.components.onewire_sysbus.onewirehub.os.path.isdir",
        return_value=True,
    ):
        yield
