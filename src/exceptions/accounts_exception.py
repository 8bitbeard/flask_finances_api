from src.exceptions.base_exception import APIError


class AccountNotFound(APIError):
    status_code = 404
    code = "NOT_FOUND"
    details = "The given account was not found!"


class AccountInvalidName(APIError):
    status_code = 400
    code = "INVALID_NAME"
    details = "The account name must be bigger than 3 and less than 80 chars"