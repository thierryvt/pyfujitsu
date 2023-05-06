import enum


# version 1.0.4

class OperationMode(enum.IntEnum):
    OFF = 0
    ON = 1
    AUTO = 2
    COOL = 3
    DRY = 4
    FAN = 5
    HEAT = 6

    def __str__(self):
        return str(self._value_)


class OperationModeDescriptors(enum.Enum):
    OFF = 'OFF'
    ON = 'ON'
    AUTO = 'AUTO'
    COOL = 'COOL'
    DRY = 'DRY'
    FAN = 'FAN'
    HEAT = 'HEAT'

    def __str__(self):
        return self._value_


VALUE_TO_OPERATION_MODE = {
    0: OperationModeDescriptors.OFF,
    1: OperationModeDescriptors.ON,
    2: OperationModeDescriptors.AUTO,
    3: OperationModeDescriptors.COOL,
    4: OperationModeDescriptors.DRY,
    5: OperationModeDescriptors.FAN,
    6: OperationModeDescriptors.HEAT
}


class FanSpeed(enum.IntEnum):
    QUIET = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    AUTO = 4

    def __str__(self):
        return str(self._value_)


class FanSpeedDescriptors(enum.Enum):
    QUIET = 'QUIET'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    AUTO = 'AUTO'

    def __str__(self):
        return self._value_


VALUE_TO_FAN_SPEED = {
    0: FanSpeedDescriptors.QUIET,
    1: FanSpeedDescriptors.LOW,
    2: FanSpeedDescriptors.MEDIUM,
    3: FanSpeedDescriptors.HIGH,
    4: FanSpeedDescriptors.AUTO
}


class BooleanProperty(enum.IntEnum):
    OFF = 0
    ON = 1

    def __str__(self):
        return str(self._value_)


class BooleanDescriptors(enum.Enum):
    ON = 'ON'
    OFF = 'OFF'

    def __str__(self):
        return self._value_


VALUE_TO_BOOLEAN = {
    0: BooleanDescriptors.OFF,
    1: BooleanDescriptors.ON
}


class VerticalSwingPosition(enum.IntEnum):
    HIGHEST = 1
    HIGH = 2
    CENTER_HIGH = 3
    CENTER_LOW = 4
    LOW = 5
    LOWEST = 6

    def __str__(self):
        return str(self._value_)


class VerticalPositionDescriptors(enum.Enum):
    HIGHEST = 'HIGHEST'
    HIGH = 'HIGH'
    CENTER_HIGH = 'CENTER_HIGH'
    CENTER_LOW = 'CENTER_LOW'
    LOW = 'LOW'
    LOWEST = 'LOWEST'

    def __str__(self):
        return self._value_


VALUE_TO_VERTICAL_POSITION = {
    1: VerticalPositionDescriptors.HIGHEST,
    2: VerticalPositionDescriptors.HIGH,
    3: VerticalPositionDescriptors.CENTER_HIGH,
    4: VerticalPositionDescriptors.CENTER_LOW,
    5: VerticalPositionDescriptors.LOW,
    6: VerticalPositionDescriptors.LOWEST
}


class ACProperties(enum.Enum):
    OPERATION_MODE = 'operation_mode'
    FAN_SPEED = 'fan_speed'
    REFRESH_READ_PROPERTIES = 'get_prop'
    VERTICAL_SWING = 'af_vertical_swing'
    VERTICAL_DIRECTION = 'af_vertical_direction'
    ADJUST_TEMPERATURE = 'adjust_temperature'
    POWERFUL_MODE = 'powerful_mode'
    ECONOMY_MODE = 'economy_mode'

    # below are readonly properties
    DISPLAY_TEMPERATURE = 'display_temperature'
    # Unclear what this does, seems to somewhat correlate to af_vertical_direction but not entirely
    VERTICAL_SWING_POSITION = 'af_vertical_num_dir'
    DEVICE_NAME = 'device_name'

    def __str__(self):
        return self._value_
