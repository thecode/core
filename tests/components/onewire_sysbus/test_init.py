"""Tests for 1-Wire config flow."""
import logging

import pytest

from homeassistant.components.onewire_sysbus.const import DOMAIN
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant


@pytest.mark.usefixtures("sysbus")
async def test_warning_no_devices(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    caplog: pytest.LogCaptureFixture,
):
    """Test warning is generated when no sysbus devices found."""
    with caplog.at_level(
        logging.WARNING, logger="homeassistant.components.onewire_sysbus"
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert "No onewire sensor found. Check if dtoverlay=w1-gpio" in caplog.text


@pytest.mark.usefixtures("sysbus")
async def test_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Test being able to unload an entry."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)
