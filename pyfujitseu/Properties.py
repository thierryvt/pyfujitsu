import enum


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


VALUE_TO_OPERATION_MODE = {
    0: 'OFF',
    1: 'ON',
    2: 'AUTO',
    3: 'COOL',
    4: 'DRY',
    5: 'FAN',
    6: 'HEAT'
}


class FanSpeed(enum.IntEnum):
    QUIET = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    AUTO = 4

    def __str__(self):
        return str(self._value_)

VALUE_TO_FAN_SPEED = {
    0: 'QUIET',
    1: 'LOW',
    2: 'MEDIUM',
    3: 'HIGH',
    4: 'AUTO'
}


class BooleanProperty(enum.IntEnum):
    OFF = 0
    ON = 1

    def __str__(self):
        return str(self._value_)


VALUE_TO_BOOLEAN = {
    0: 'OFF',
    1: 'ON'
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


VALUE_TO_VERTICAL_POSITION = {
    1: 'HIGHEST',
    2: 'HIGH',
    3: 'CENTER_HIGH',
    4: 'CENTER_LOW',
    5: 'LOW',
    6: 'LOWEST'
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
    VERTICAL_SWING_POSITION = 'af_vertical_num_dir'
    DEVICE_NAME = 'device_name'

    def __str__(self):
        return self._value_
