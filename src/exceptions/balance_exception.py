from src.exceptions.base_exception import APIError


class BalanceInvalid(APIError):
    status_code = 400
    code = "INVALID_BALANCE"
    details = "Balance value must be numeric!"