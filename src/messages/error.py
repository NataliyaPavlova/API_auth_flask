from enum import Enum


class AuthError(str, Enum):
    MISSING_LOGIN = 'No login in request'
    MISSING_PWD = 'No password in request'
    USER_EXISTED = 'User with these credentials already exists'
    USER_NOT_FOUND = 'User with these credentials not found'
    NO_ACCESS_TOKEN = 'Access-Token is missing'
    NO_REFRESH_TOKEN = 'Refresh-Token is missing'
    EXPIRED_TOKENS = 'Tokens are expired. Login is needed.'


class ProfileError(str, Enum):
    MISSING_LOGIN = 'No login in request'
    NO_INFO_TO_CHANGE = 'No info to change: new login or new pwd should be in request'
    USER_EXISTED = 'User with such new login is already existed'
