"""
Transactions Custom Exceptions
"""

from src.exceptions.base_exception import APIError


class TransactionValueNegativeOrZero(APIError):
    """
    Invalid value transaction Exception
    """
    status_code = 400
    code = "INVALID_VALUE"
    details = "Transaction values must be bigger than 0!"
