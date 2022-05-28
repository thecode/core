"""Constants for 1-Wire integration."""
from pi1wire import InvalidCRCException, UnsupportResponseException

from homeassistant.components.onewire_sysbus.const import (
    DOMAIN,
    MANUFACTURER_MAXIM,
    Platform,
)
from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ENTITY_ID,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME,
    ATTR_STATE,
    ATTR_UNIT_OF_MEASUREMENT,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
)

ATTR_DEFAULT_DISABLED = "default_disabled"
ATTR_DEVICE_FILE = "device_file"
ATTR_DEVICE_INFO = "device_info"
ATTR_ENTITY_CATEGORY = "entity_category"
ATTR_INJECT_READS = "inject_reads"
ATTR_UNIQUE_ID = "unique_id"
ATTR_UNKNOWN_DEVICE = "unknown_device"

FIXED_ATTRIBUTES = (
    ATTR_DEVICE_CLASS,
    ATTR_STATE_CLASS,
    ATTR_UNIT_OF_MEASUREMENT,
)


MOCK_SYSBUS_DEVICES = {
    "00-111111111111": {
        ATTR_UNKNOWN_DEVICE: True,
    },
    "10-111111111111": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "10-111111111111")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "10",
            ATTR_NAME: "10-111111111111",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.10_111111111111_temperature",
                ATTR_INJECT_READS: 25.123,
                ATTR_STATE: "25.1",
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/10-111111111111/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "22-111111111111": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "22-111111111111")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "22",
            ATTR_NAME: "22-111111111111",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.22_111111111111_temperature",
                ATTR_INJECT_READS: FileNotFoundError,
                ATTR_STATE: STATE_UNKNOWN,
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/22-111111111111/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "28-111111111111": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "28-111111111111")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "28",
            ATTR_NAME: "28-111111111111",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.28_111111111111_temperature",
                ATTR_INJECT_READS: InvalidCRCException,
                ATTR_STATE: STATE_UNKNOWN,
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/28-111111111111/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "3B-111111111111": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "3B-111111111111")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "3B",
            ATTR_NAME: "3B-111111111111",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.3b_111111111111_temperature",
                ATTR_INJECT_READS: 29.993,
                ATTR_STATE: "30.0",
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/3B-111111111111/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "42-111111111111": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "42-111111111111")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "42",
            ATTR_NAME: "42-111111111111",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.42_111111111111_temperature",
                ATTR_INJECT_READS: UnsupportResponseException,
                ATTR_STATE: STATE_UNKNOWN,
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/42-111111111111/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "42-111111111112": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "42-111111111112")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "42",
            ATTR_NAME: "42-111111111112",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.42_111111111112_temperature",
                ATTR_INJECT_READS: [UnsupportResponseException] * 9 + [27.993],
                ATTR_STATE: "28.0",
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/42-111111111112/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
    "42-111111111113": {
        ATTR_DEVICE_INFO: {
            ATTR_IDENTIFIERS: {(DOMAIN, "42-111111111113")},
            ATTR_MANUFACTURER: MANUFACTURER_MAXIM,
            ATTR_MODEL: "42",
            ATTR_NAME: "42-111111111113",
        },
        Platform.SENSOR: [
            {
                ATTR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
                ATTR_ENTITY_ID: "sensor.42_111111111113_temperature",
                ATTR_INJECT_READS: [UnsupportResponseException] * 10 + [27.993],
                ATTR_STATE: STATE_UNKNOWN,
                ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT,
                ATTR_UNIQUE_ID: "/sys/bus/w1/devices/42-111111111113/w1_slave",
                ATTR_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
            },
        ],
    },
}
