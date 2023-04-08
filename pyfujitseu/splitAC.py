from .api import Api as api
from properties import *


# version 0.9.2.7

class splitAC:
    def __init__(self, dsn, api):
        self._dsn = dsn
        self._api = api
        self._properties = self._api.get_device_properties(self._dsn)

    def refresh_properties(self):
        self._properties = self._api.get_device_properties(self._dsn)

    def _set_device_property(self, propertyCode: ACProperties, value):
        self._api.set_device_property(self._dsn, propertyCode, value)

    def _get_device_property(self, propertyCode: ACProperties):
        return self._api.get_device_properties(self._dsn, propertyCode)

    def _get_device_property_value(self, propertyCode: ACProperties):
        return self._get_device_property(propertyCode)['value']

    # special case, props like display temperature do not update automatically
    # sending this property triggers it to update
    # calling refresh_properties technically achieves the same because it pushes ALL the properties, including this one
    def refresh_readonly_properties(self):
        self._set_device_property(ACProperties.REFRESH_READ_PROPERTIES, BooleanProperty.ON)

    def turn_on(self, mode: OperationMode):
        self._set_device_property(ACProperties.OPERATION_MODE, mode)

    def turn_off(self):
        self._set_device_property(ACProperties.OPERATION_MODE, OperationMode.OFF)

    def set_economy_mode_on(self):
        self._set_device_property(ACProperties.ECONOMY_MODE, BooleanProperty.ON)

    def set_economy_mode_off(self):
        self._set_device_property(ACProperties.ECONOMY_MODE, BooleanProperty.OFF)

    def set_powerful_mode_on(self):
        self._set_device_property(ACProperties.POWERFUL_MODE, BooleanProperty.ON)

    def set_powerful_mode_off(self):
        self._set_device_property(ACProperties.POWERFUL_MODE, BooleanProperty.OFF)

    def set_fan_speed(self, speed: FanSpeed):
        print(speed)
        self._set_device_property(ACProperties.FAN_SPEED, speed)

    def get_fan_speed_desc(self):
        return FAN_SPEED_DICT[self._get_device_property_value(ACProperties.FAN_SPEED)]

    def set_vertical_direction(self, direction: VerticalSwingPosition):
        self._set_device_property(ACProperties.VERTICAL_DIRECTION, direction)

    def get_vertical_direction(self):
        return self._get_device_property_value(ACProperties.VERTICAL_SWING_POSITION)

    def set_vertical_swing_on(self):
        self._set_device_property(ACProperties.VERTICAL_SWING, BooleanProperty.ON)

    def set_vertical_swing_off(self):
        self._set_device_property(ACProperties.VERTICAL_SWING, BooleanProperty.OFF)

    # TODO detect if C or F is being used but I'm lazy AF and Celsius is best unit anyway
    # display temperature is x100 and has an offset of 5400 for... reasons.
    def get_display_temperature(self):
        return (int(self._get_device_property_value(ACProperties.DISPLAY_TEMPERATURE)) - 5400) / 100

    # and if you thought that setting the temperature was the same? Hah. No.
    # when using C you need to set the target temperature x10
    def set_target_temperature(self, targetTemperature: float):
        if targetTemperature < 16.0 or targetTemperature > 30.0:
            raise Exception('Invalid targetTemperature, must be 16 <= target <= 30')

        actualTarget = int(targetTemperature * 10)
        self._set_device_property(ACProperties.ADJUST_TEMPERATURE, actualTarget)
