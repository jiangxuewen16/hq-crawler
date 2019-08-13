from enum import Enum, unique


@unique
class ResponseHandleType(Enum):
    JS = 'application/x-javascript'
    HTML = 'text/html'
    JSON = 'application/json'
