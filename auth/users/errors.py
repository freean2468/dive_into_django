from enum import Enum


class Errors(Enum):
    SIGNIN_NOT_VALID_ID = 1,
    SIGNIN_LACK_OF_POST_DATA = 2,
    SIGNIN_NOT_VALID_PASSWORD = 3,


def ec(error_code):
    return {'error_code': error_code.value}
