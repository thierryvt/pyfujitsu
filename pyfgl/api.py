import logging
import requests
import time
import os
import json
import enum

HEADER_CONTENT_TYPE = "Content-Type"
HEADER_VALUE_CONTENT_TYPE = "application/json"
HEADER_AUTHORIZATION = "Authorization"

# version 1.0.1

_LOGGER = logging.getLogger(__name__)


def _api_headers(access_token=None):
    headers = {
        HEADER_CONTENT_TYPE: HEADER_VALUE_CONTENT_TYPE
    }

    if access_token:
        headers[HEADER_AUTHORIZATION] = 'auth_token ' + access_token

    return headers

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
    VERTICAL_SWING_POSITION = 'af_vertical_num_dir'
    DEVICE_NAME = 'device_name'

    def __str__(self):
        return self._value_



class Api:
    def __init__(self, username, password, region='us', tokenpath='token.txt'):
        self.username = username
        self.password = password
        self.region = region

        if region == 'eu':
            self._SIGNIN_BODY = '{"user":{"email":"%s","password":"%s","application":{"app_id":"FGLair-eu-id","app_secret":"FGLair-eu-gpFbVBRoiJ8E3QWJ-QRULLL3j3U"}}}'
            self._API_GET_ACCESS_TOKEN_URL = "https://user-field-eu.aylanetworks.com/users/sign_in.json"
            API_BASE_URL = "https://ads-field-eu.aylanetworks.com/apiv1/"
        elif region == 'cn':
            self._SIGNIN_BODY = '{"user":{"email":"%s","password":"%s","application":{"app_id":"FGLairField-cn-id","app_secret":"FGLairField-cn-zezg7Y60YpAvy3HPwxvWLnd4Oh4"}}}'
            self._API_GET_ACCESS_TOKEN_URL = "https://user-field.ayla.com.cn/users/sign_in.json"
            API_BASE_URL = "https://ads-field.ayla.com.cn/apiv1/"
        else:
            self._SIGNIN_BODY = '{"user": {"email": "%s", "application": {"app_id": "CJIOSP-id", "app_secret": "CJIOSP-Vb8MQL_lFiYQ7DKjN0eCFXznKZE"},"password": "%s" }}'
            self._API_GET_ACCESS_TOKEN_URL = "https://user-field.aylanetworks.com/users/sign_in.json"
            API_BASE_URL = "https://ads-field.aylanetworks.com/apiv1/"

        self._API_GET_PROPERTIES_URL = API_BASE_URL + "dsns/{DSN}/properties.json"
        self._API_GET_PROPERTY_URL = API_BASE_URL + "dsns/{DSN}/properties/{property}.json"
        self._API_SET_PROPERTY_URL = API_BASE_URL + "dsns/{DSN}/properties/{property}/datapoints.json"
        self._API_GET_DEVICES_URL = API_BASE_URL + "devices.json"

        self._ACCESS_TOKEN_FILE = tokenpath

    def get_devices(self, access_token=None):
        if not self._check_token_validity(access_token):
            ## Token invalid requesting authentication
            access_token = self._authenticate()
        response = self._call_api("get", self._API_GET_DEVICES_URL, access_token=access_token)
        return response.json()

    def get_devices_dsn(self, access_token=None):
        devices = self.get_devices()
        devices_dsn = []
        for device in devices:
            devices_dsn.append(device['device']['dsn'])
        return devices_dsn

    def get_device_properties(self, dsn):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("get", self._API_GET_PROPERTIES_URL.format(DSN=dsn), access_token=access_token)
        return response.json()

    def set_device_property(self, dsn, propertyCode: ACProperties, value):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("post", self._API_SET_PROPERTY_URL.format(DSN=dsn, property=propertyCode),
                                  propertyValue=value, access_token=access_token)

        return response

    def get_device_property(self, dsn, propertyCode: ACProperties):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("get", self._API_GET_PROPERTY_URL.format(DSN=dsn, property=propertyCode),
                                  access_token=access_token)

        return response.json()

    def get_device_property_history(self, dsn, propertyCode: ACProperties):
        access_token = self._read_token()
        if not self._check_token_validity(access_token):
            access_token = self._authenticate()

        response = self._call_api("get", self._API_SET_PROPERTY_URL.format(DSN=dsn, property=propertyCode),
                                  access_token=access_token)
        ## Pay Attention the response is a HTTP request response object
        #  and by doing .json you would get a List
        return response

    def _check_token_validity(self, access_token=None):
        if not access_token:
            return False
        try:
            self._call_api("get", self._API_GET_DEVICES_URL, access_token=access_token)
        except:
            return False
        return True

    def _authenticate(self):
        body = self._SIGNIN_BODY % (self.username, self.password)
        response = self._call_api("POST",
                                  self._API_GET_ACCESS_TOKEN_URL,
                                  json=self._SIGNIN_BODY % (self.username, self.password),
                                  headers=_api_headers())

        response.json()['time'] = int(time.time())

        access_token = response.json()['access_token']

        # refresh_token = response.json()['refresh_token']
        # expires_in = response.json()['expires_in']

        f = open(self._ACCESS_TOKEN_FILE, "w")
        f.write(response.text)

        return access_token

    def _read_token(self, access_token_file=None):
        if not access_token_file:
            access_token_file = self._ACCESS_TOKEN_FILE
        if (os.path.exists(access_token_file) and os.stat(access_token_file).st_size != 0):
            f = open(access_token_file, "r")
            access_token_file_content = f.read()

            # now = int(time.time())

            access_token = json.loads(access_token_file_content)['access_token']
            # refresh_token = access_token_file_content.json()['refresh_token']
            # expires_in = access_token_file_content.json()['expires_in']
            # auth_time = int(access_token_file_content.json()['time'])
            return access_token
        else:
            return self._authenticate()

    def _call_api(self, method, url, access_token=None, **kwargs):
        payload = ''

        if "propertyValue" in kwargs:
            propertyValue = kwargs.get("propertyValue")
            kwargs["json"] = '{\"datapoint\": {\"value\": ' + str(propertyValue) + ' } }'
        payload = kwargs.get("json")

        if "headers" not in kwargs:
            if access_token:
                kwargs["headers"] = _api_headers(access_token=access_token)
            else:
                kwargs["headers"] = _api_headers()

        if method.lower() == 'post':
            if not payload:
                raise Exception('Post method needs a request body!')

        response = requests.request(method, url, data=kwargs.get("json"), headers=kwargs.get("headers"))
        response.raise_for_status()
        return response