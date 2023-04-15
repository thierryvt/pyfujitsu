from .constants import *
import time


# version 1.0.1

class SplitAC:
    def __init__(self, dsn, api):
        if not api:
            raise Exception('Missing api')

        if not dsn or not isinstance(dsn, str):
            raise ValueError("dsn must be a non-empty string")

        self._dsn = dsn
        self._api = api
        self._cache = {}

    def _set_device_property(self, propertyCode: ACProperties, value):
        if not isinstance(propertyCode, ACProperties):
            raise Exception(f"Invalid propertyCode: {propertyCode}")

        self._api.set_device_property(self._dsn, propertyCode, value)
        if propertyCode in self._cache:
            del self._cache[propertyCode]
        self._get_device_property(propertyCode)

    def _get_device_property(self, propertyCode: ACProperties):
        if not isinstance(propertyCode, ACProperties):
            raise Exception(f"Invalid propertyCode: {propertyCode}")

        if propertyCode in self._cache:
            return self._cache[propertyCode]

        result = self._api.get_device_property(self._dsn, propertyCode)
        self._cache[propertyCode] = result
        return result

    def _get_device_property_value(self, propertyCode: ACProperties):
        if not isinstance(propertyCode, ACProperties):
            raise Exception(f"Invalid propertyCode: {propertyCode}")

        # return self._get_device_property(propertyCode)['property']['value']
        return self._cache[propertyCode]['property']['value']

    def refresh_properties(self):
        self._cache.clear()
        # refresh read-only properties like the display_temperature
        self._set_device_property(ACProperties.REFRESH_READ_PROPERTIES, BooleanProperty.ON)
        # synchronized sleep, block that mainthread. HA will wrap this in an asynchronous thingy anyway.
        time.sleep(3)
        properties = self._api.get_device_properties(self._dsn)
        for property in properties:
            try:
                name = property['property']['name']
                value = property['property']['value']
                propertyCode = ACProperties(name)
                self._cache[propertyCode] = value
            except ValueError:
                pass

    def get_device_name(self):
        return self._get_device_property_value(ACProperties.DEVICE_NAME)

    def turn_on(self):
        datapoints = self._api.get_device_property_history(self._dsn, ACProperties.OPERATION_MODE)
        # Get the last operation_mode that was not 'off'
        for datapoint in reversed(datapoints):
            if datapoint['datapoint']['value'] != OperationMode.OFF:
                last_operation_mode = int(datapoint['datapoint']['value'])
                break

        self.set_operation_mode(last_operation_mode)

    def turn_off(self):
        self._set_device_property(ACProperties.OPERATION_MODE, OperationMode.OFF)

    def get_operating_mode(self):
        return VALUE_TO_OPERATION_MODE[self._get_device_property_value(ACProperties.OPERATION_MODE)]

    def set_operation_mode(self, mode: OperationMode):
        if not isinstance(mode, OperationMode):
            raise Exception(f'Invalid operationMode value: {mode}')
        self._set_device_property(ACProperties.OPERATION_MODE, mode)

    def set_economy_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.ECONOMY_MODE, mode)

    def get_economy_mode(self):
        return VALUE_TO_BOOLEAN[self._get_device_property_value(ACProperties.ECONOMY_MODE)]

    def set_powerful_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.POWERFUL_MODE, mode)

    def get_powerful_mode(self):
        return VALUE_TO_BOOLEAN[self._get_device_property_value(ACProperties.POWERFUL_MODE)]

    def set_fan_speed(self, speed: FanSpeed):
        if not isinstance(speed, FanSpeed):
            raise Exception(f'Invalid fan speed value: {speed}')
        self._set_device_property(ACProperties.FAN_SPEED, speed)

    def get_fan_speed(self):
        return VALUE_TO_FAN_SPEED[self._get_device_property_value(ACProperties.FAN_SPEED)]

    def set_vertical_direction(self, direction: VerticalSwingPosition):
        if not isinstance(direction, VerticalSwingPosition):
            raise Exception(f'Invalid fan direction value: {direction}')
        self._set_device_property(ACProperties.VERTICAL_DIRECTION, direction)

    def get_vertical_direction(self):
        return VALUE_TO_VERTICAL_POSITION[self._get_device_property_value(ACProperties.VERTICAL_SWING_POSITION)]

    def set_vertical_swing(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.VERTICAL_SWING, mode)

    def get_vertical_swing(self):
        return VALUE_TO_BOOLEAN[self._get_device_property_value(ACProperties.VERTICAL_SWING)]

    # TODO detect if C or F is being used but I'm lazy AF and Celsius is best unit anyway
    # display temperature is x100 and has an offset of 5000 for... reasons.
    def get_display_temperature(self):
        return (int(self._get_device_property_value(ACProperties.DISPLAY_TEMPERATURE)) - 5000) / 100

    # and if you thought that setting the temperature was the same? Hah. No.
    # you need to set the target temperature x10
    def set_target_temperature(self, targetTemperature: float):
        if targetTemperature < 16.0 or targetTemperature > 30.0:
            raise Exception(f'Invalid targetTemperature: {targetTemperature}. Value must be 16 <= target <= 30')

        actualTarget = int(targetTemperature * 10)
        self._set_device_property(ACProperties.ADJUST_TEMPERATURE, actualTarget)

    def get_target_temperature(self):
        return int(self._get_device_property_value(ACProperties.ADJUST_TEMPERATURE)) / 10
