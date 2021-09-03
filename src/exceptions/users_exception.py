"""
Users Custom Exceptions
"""

from src.exceptions.base_exception import APIError


class UserMissingParameter(APIError):
    """
    Missing parameter Exception
    """
    status_code = 400
    code = "MISSING_PARAMETER"
    details = "Missing mandatory parameters!"


class UserNameInvalid(APIError):
    """
    Invalid name exception
    """
    status_code = 400
    code = "INVALID_NAME"
    details = "Provided name is invalid!"


class UserEmailInvalid(APIError):
    """
    Invalid email exception
    """
    status_code = 400
    code = "INVALID_EMAIL"
    details = "Provided email is invalid!"


class UserEmailAlreadyExists(APIError):
    """
    Already taken email exception
    """
    status_code = 409
    code = "EMAIL_ALREADY_EXISTS"
    details = "This email is already taken!"


class UserNotFound(APIError):
    """
    User not found exception
    """
    status_code = 404
    code = "NOT_FOUND"
    details = "User not found!"


class UserPasswordTooShort(APIError):
    """
    Invalid password exception
    """
    status_code = 400
    code = "INVALID_PASSWORD"
    details = "Provided password is invalid!"
