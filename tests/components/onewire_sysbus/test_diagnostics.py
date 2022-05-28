"""Test 1-Wire diagnostics."""
from unittest.mock import patch

import pytest

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from . import setup_sysbus_mock_devices

from tests.components.diagnostics import get_diagnostics_for_config_entry


@pytest.fixture(autouse=True)
def override_platforms():
    """Override PLATFORMS."""
    with patch("homeassistant.components.onewire_sysbus.PLATFORMS", [Platform.SENSOR]):
        yield


DEVICE_DETAILS = {
    "identifiers": [["onewire_sysbus", "10-111111111111"]],
    "manufacturer": "Maxim Integrated",
    "model": "10",
    "name": "10-111111111111",
}


@pytest.mark.usefixtures("sysbus")
@pytest.mark.parametrize("device_id", ["10-111111111111"], indirect=True)
async def test_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    hass_client,
    device_id: str,
):
    """Test config entry diagnostics."""
    setup_sysbus_mock_devices(Platform.SENSOR, [device_id])

    glob_result, read_side_effect = setup_sysbus_mock_devices(
        Platform.SENSOR, [device_id]
    )

    with patch("pi1wire._finder.glob.glob", return_value=glob_result,), patch(
        "pi1wire.OneWire.get_temperature",
        side_effect=read_side_effect,
    ), patch("homeassistant.components.onewire_sysbus.sensor.asyncio.sleep"):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert await get_diagnostics_for_config_entry(
            hass, hass_client, config_entry
        ) == {
            "entry": {
                "data": {"mount_dir": "/sys/bus/w1/devices/"},
                "title": "Mock Title",
            },
            "devices": [DEVICE_DETAILS],
        }
