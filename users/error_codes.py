from enum import Enum

class ErrorCodes(Enum):
    SIGNIN_NOT_VALID_ID = 1,
    SIGNIN_LACK_OF_POST_DATA = 2,
    SIGNIN_NOT_VALID_PASSWORD = 3,