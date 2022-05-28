"""Tests for 1-Wire integration."""
from __future__ import annotations

from types import MappingProxyType
from typing import Any

from homeassistant.components.onewire_sysbus.const import DEFAULT_SYSBUS_MOUNT_DIR
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME,
    ATTR_STATE,
    ATTR_VIA_DEVICE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.helpers.entity_registry import EntityRegistry

from .const import (
    ATTR_DEVICE_FILE,
    ATTR_ENTITY_CATEGORY,
    ATTR_INJECT_READS,
    ATTR_UNIQUE_ID,
    FIXED_ATTRIBUTES,
    MOCK_SYSBUS_DEVICES,
)


def check_device_registry(
    device_registry: DeviceRegistry, expected_devices: list[MappingProxyType]
) -> None:
    """Ensure that the expected_devices are correctly registered."""
    for expected_device in expected_devices:
        registry_entry = device_registry.async_get_device(
            expected_device[ATTR_IDENTIFIERS]
        )
        assert registry_entry is not None
        assert registry_entry.identifiers == expected_device[ATTR_IDENTIFIERS]
        assert registry_entry.manufacturer == expected_device[ATTR_MANUFACTURER]
        assert registry_entry.name == expected_device[ATTR_NAME]
        assert registry_entry.model == expected_device[ATTR_MODEL]
        if expected_via_device := expected_device.get(ATTR_VIA_DEVICE):
            assert registry_entry.via_device_id is not None
            parent_entry = device_registry.async_get_device({expected_via_device})
            assert parent_entry is not None
            assert registry_entry.via_device_id == parent_entry.id
        else:
            assert registry_entry.via_device_id is None


def check_entities(
    hass: HomeAssistant,
    entity_registry: EntityRegistry,
    expected_entities: MappingProxyType,
) -> None:
    """Ensure that the expected_entities are correct."""
    for expected_entity in expected_entities:
        entity_id = expected_entity[ATTR_ENTITY_ID]
        registry_entry = entity_registry.entities.get(entity_id)
        assert registry_entry is not None
        assert registry_entry.entity_category == expected_entity.get(
            ATTR_ENTITY_CATEGORY
        )
        assert registry_entry.unique_id == expected_entity[ATTR_UNIQUE_ID]
        state = hass.states.get(entity_id)
        assert state.state == expected_entity[ATTR_STATE]
        assert state.attributes[ATTR_DEVICE_FILE] == expected_entity.get(
            ATTR_DEVICE_FILE, registry_entry.unique_id
        )
        for attr in FIXED_ATTRIBUTES:
            assert state.attributes.get(attr) == expected_entity.get(attr)


def setup_sysbus_mock_devices(
    platform: str, device_ids: list[str]
) -> tuple[list[str], list[Any]]:
    """Set up mock for sysbus."""
    glob_result = []
    read_side_effect = []

    for device_id in device_ids:
        mock_device = MOCK_SYSBUS_DEVICES[device_id]

        # Setup directory listing
        glob_result += [f"/{DEFAULT_SYSBUS_MOUNT_DIR}/{device_id}"]

        # Setup sub-device reads
        device_sensors = mock_device.get(platform, [])
        for expected_sensor in device_sensors:
            if isinstance(expected_sensor[ATTR_INJECT_READS], list):
                read_side_effect += expected_sensor[ATTR_INJECT_READS]
            else:
                read_side_effect.append(expected_sensor[ATTR_INJECT_READS])

    # Ensure enough read side effect
    read_side_effect.extend([FileNotFoundError("Missing injected value")] * 20)

    return (glob_result, read_side_effect)
