"""
Authentication Custom Exceptions
"""

from src.exceptions.base_exception import APIError


class AuthenticationBadCredentials(APIError):
    """
    Bad Credentials Exception
    """
    status_code = 401
    code = "UNAUTHORIZED"
    details = "Wrong credentials!"
