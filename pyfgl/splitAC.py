from .constants import *
from datetime import datetime, timedelta

# version 1.0.5

class SplitAC:
    def __init__(self, dsn, api):
        if not api:
            raise Exception('Missing api')

        if not dsn or not isinstance(dsn, str):
            raise ValueError("dsn must be a non-empty string")

        self._dsn = dsn
        self._api = api
        self._cache = {}
        self._min_temp = 16.0
        self._max_temp = 30.0
        self._last_update = datetime.now() - timedelta(minutes=15)

    def _set_device_property(self, property_code: ACProperties, value):
        if not isinstance(property_code, ACProperties):
            raise Exception(f"Invalid propertyCode: {property_code}")

        self._api.set_device_property(self._dsn, property_code, value)
        self._cache[property_code] = value

    def _get_raw_device_property_from_api(self, property_code: ACProperties):
        if not isinstance(property_code, ACProperties):
            raise Exception(f"Invalid propertyCode: {property_code}")

        return self._api.get_device_property(self._dsn, property_code)

    def _get_cached_device_property(self, property_code: ACProperties):
        if not isinstance(property_code, ACProperties):
            raise Exception(f"Invalid propertyCode: {property_code}")

        if property_code in self._cache:
            return self._cache[property_code]
        else:
            return 'N/A'

    def refresh_properties(self):
        current_time = datetime.now()
        if current_time - self._last_update < timedelta(minutes=10):
            return

        # refresh read-only properties like the display_temperature, takes a second or 2 so might not update in time
        self._set_device_property(ACProperties.REFRESH_READ_PROPERTIES, BooleanProperty.ON)
        properties = self._api.get_device_properties(self._dsn)

        self._last_update = current_time

        # adjust_temperature values are returned as a x10 value
        min_temp_raw = self._min_temp * 10
        max_temp_raw = self._max_temp * 10
        for property in properties:
            try:
                name = property['property']['name']
                value = property['property']['value']
                property_code = ACProperties(name)
                # this property comes back as 0 after the AC has been off for a while.
                # either ignore it if it's already in the cache, otherwise try to determine what the last known value was
                if property_code == ACProperties.ADJUST_TEMPERATURE and (value < min_temp_raw or value > max_temp_raw):
                    if property_code in self._cache:
                        continue
                    else:
                        value = self._get_last_known_value_for_property_not_equal_to_or_else_default(ACProperties.ADJUST_TEMPERATURE, 0, 0)

                self._cache[property_code] = value
            except ValueError:
                pass

    # finds the most recent known value of a property that is not equal to the given value
    # If no such value can be found the default_value is returned
    def _get_last_known_value_for_property_not_equal_to_or_else_default(self, property_code: ACProperties, value, default_value):
        if not isinstance(property_code, ACProperties):
            raise Exception(f"Invalid propertyCode: {property_code}")

        datapoints = self._api.get_device_property_history(self._dsn, property_code)
        last_value = default_value
        for datapoint in reversed(datapoints.json()):
            if datapoint['datapoint']['value'] != value:
                last_value = datapoint['datapoint']['value']
                break
        return last_value

    def get_device_name(self):
        return self._get_cached_device_property(ACProperties.DEVICE_NAME)

    def turn_on(self):
        raw = self._get_last_known_value_for_property_not_equal_to_or_else_default(ACProperties.OPERATION_MODE, OperationMode.OFF, OperationMode.AUTO)
        last_operation_mode = VALUE_TO_OPERATION_MODE[raw]
        self.set_operation_mode(last_operation_mode)

    def turn_off(self):
        self._set_device_property(ACProperties.OPERATION_MODE, OperationMode.OFF)

    def get_operating_mode(self):
        return VALUE_TO_OPERATION_MODE[self._get_cached_device_property(ACProperties.OPERATION_MODE)]

    def set_operation_mode(self, mode: OperationMode):
        if not isinstance(mode, OperationMode):
            raise Exception(f'Invalid operationMode value: {mode}')
        self._set_device_property(ACProperties.OPERATION_MODE, mode)

    def set_economy_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.ECONOMY_MODE, mode)

    def get_economy_mode(self):
        return VALUE_TO_BOOLEAN[self._get_cached_device_property(ACProperties.ECONOMY_MODE)]

    def set_powerful_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.POWERFUL_MODE, mode)

    def get_powerful_mode(self):
        return VALUE_TO_BOOLEAN[self._get_cached_device_property(ACProperties.POWERFUL_MODE)]

    def set_fan_speed(self, speed: FanSpeed):
        if not isinstance(speed, FanSpeed):
            raise Exception(f'Invalid fan speed value: {speed}')
        self._set_device_property(ACProperties.FAN_SPEED, speed)

    def get_fan_speed(self):
        return VALUE_TO_FAN_SPEED[self._get_cached_device_property(ACProperties.FAN_SPEED)]

    def set_vertical_direction(self, direction: VerticalSwingPosition):
        if not isinstance(direction, VerticalSwingPosition):
            raise Exception(f'Invalid fan direction value: {direction}')
        self._set_device_property(ACProperties.VERTICAL_DIRECTION, direction)
        self.set_vertical_swing(BooleanProperty.OFF)

    def get_vertical_direction(self):
        return VALUE_TO_VERTICAL_POSITION[self._get_cached_device_property(ACProperties.VERTICAL_DIRECTION)]

    def set_vertical_swing(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f'Invalid mode value: {mode}')
        self._set_device_property(ACProperties.VERTICAL_SWING, mode)

    def get_vertical_swing(self):
        return VALUE_TO_BOOLEAN[self._get_cached_device_property(ACProperties.VERTICAL_SWING)]

    # TODO detect if C or F is being used but I'm lazy AF and Celsius is best unit anyway
    # display temperature is x100 and has an offset of 5000 for... reasons.
    def get_display_temperature(self):
        return (int(self._get_cached_device_property(ACProperties.DISPLAY_TEMPERATURE)) - 5000) / 100

    # and if you thought that setting the temperature was the same? Hah. No.
    # you need to set the target temperature x10
    def set_target_temperature(self, target_temperature: float):
        if target_temperature < self._min_temp or target_temperature > self._max_temp:
            raise Exception(f'Invalid targetTemperature: {target_temperature}. Value must be {self._min_temp} <= target <= {self._max_temp}')

        actual_target = int(target_temperature * 10)
        self._set_device_property(ACProperties.ADJUST_TEMPERATURE, actual_target)

    def get_target_temperature(self):
        return int(self._get_cached_device_property(ACProperties.ADJUST_TEMPERATURE)) / 10
