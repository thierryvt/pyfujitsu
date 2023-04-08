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


class FanSpeed(enum.IntEnum):
    QUIET = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    AUTO = 4

    def __str__(self):
        return str(self._value_)


class BooleanProperty(enum.IntEnum):
    OFF = 0
    ON = 1

    def __str__(self):
        return str(self._value_)


class VerticalSwingPosition(enum.IntEnum):
    UP = 1
    POS2 = 2
    POS3 = 3
    POS4 = 4
    POS5 = 5
    DOWN = 6

    def __str__(self):
        return str(self._value_)


FAN_SPEED_DICT = {
    0: 'Quiet',
    1: 'Low',
    2: 'Medium',
    3: 'High',
    4: 'Auto'
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
