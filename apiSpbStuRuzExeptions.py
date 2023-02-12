"""
This file contains exceptions that may appear during the operation of the library

Date of create file: 02.12.2023
"""


class ApiSpbStuRuzException(Exception):
    """Base class for api errors"""


class ConnectionException(ApiSpbStuRuzException):
    """Base class for connections exceptions"""


class ConvertJsonException(ApiSpbStuRuzException):
    """Base class for conversion exceptions"""


class ResponseCodeError(ConnectionException):
    """Exception with connect to server"""

    def __init__(self, path, code):
        super().__init__(f'Incorrect status code from "{path}": {code}')


class ClientConnectionError(ConnectionException):
    """Exception with connect on Client side"""

    def __init__(self, e):
        super().__init__(f'Can\'t connect to server: {e}')


class ProxyError(ConnectionException):
    """Exception with proxy"""

    def __init__(self, proxy, e):
        super().__init__(f'Invalid proxy {proxy}: {e}')


class TimeOutError(ConnectionException):
    """The response waiting time is too long"""

    def __init__(self, e):
        super().__init__(f'Waiting time exceeded: {e}')


class JsonConvertError(ConvertJsonException):
    """Can't convert JSON to dataclasses"""

    def __init__(self, json, e):
        super().__init__(f'Can\'t convert json {json}: {e}')


class JsonTypeError(ConvertJsonException):
    """Something throw TypeError in JSON convert process"""

    def __init__(self, e):
        super().__init__(f'Something went wrong in the JSON conversion process: {e}')


class JsonKeyError(ConvertJsonException):
    """
    Probably an error in the conversion function.
    In the release version this error appears only when
    changing the format of the response from the server
    """

    def __init__(self, e):
        super().__init__(f'Can\'t found key in json_file: {e}')
