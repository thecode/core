"""Tests for 1-Wire sensor platform."""
import logging
from unittest.mock import patch

import pytest

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_validation import ensure_list

from . import check_device_registry, check_entities, setup_sysbus_mock_devices
from .const import ATTR_DEVICE_INFO, ATTR_UNKNOWN_DEVICE, MOCK_SYSBUS_DEVICES

from tests.common import mock_device_registry, mock_registry


@pytest.fixture(autouse=True)
def override_platforms():
    """Override PLATFORMS."""
    with patch("homeassistant.components.onewire_sysbus.PLATFORMS", [Platform.SENSOR]):
        yield


@pytest.mark.usefixtures("sysbus")
@pytest.mark.parametrize("device_id", MOCK_SYSBUS_DEVICES.keys(), indirect=True)
async def test_onewiredirect_setup_valid_device(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    device_id: str,
    caplog: pytest.LogCaptureFixture,
):
    """Test that sysbus config entry works correctly."""
    device_registry = mock_device_registry(hass)
    entity_registry = mock_registry(hass)

    glob_result, read_side_effect = setup_sysbus_mock_devices(
        Platform.SENSOR, [device_id]
    )

    mock_device = MOCK_SYSBUS_DEVICES[device_id]
    expected_entities = mock_device.get(Platform.SENSOR, [])
    expected_devices = ensure_list(mock_device.get(ATTR_DEVICE_INFO))

    with patch("pi1wire._finder.glob.glob", return_value=glob_result,), patch(
        "pi1wire.OneWire.get_temperature",
        side_effect=read_side_effect,
    ), caplog.at_level(
        logging.WARNING, logger="homeassistant.components.onewire_sysbus"
    ), patch(
        "homeassistant.components.onewire_sysbus.sensor.asyncio.sleep"
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert "No onewire sensor found. Check if dtoverlay=w1-gpio" not in caplog.text
        if mock_device.get(ATTR_UNKNOWN_DEVICE):
            assert "Ignoring unknown device family" in caplog.text
        else:
            assert "Ignoring unknown device family" not in caplog.text

    check_device_registry(device_registry, expected_devices)
    assert len(entity_registry.entities) == len(expected_entities)
    check_entities(hass, entity_registry, expected_entities)
