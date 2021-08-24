from src.exceptions.base_exception import APIError


class AccountNotFound(APIError):
    status_code = 404
    code = "NOT_FOUND"
    details = "The given account was not found!"