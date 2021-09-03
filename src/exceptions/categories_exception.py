"""
Categories Custom Exceptions
"""

from src.exceptions.base_exception import APIError


class IncorrectCategory(APIError):
    """
    Inorrect Category Exception
    """
    status_code = 400
    code = "INCORRECT_CATEGORY"
    details = "This category cannot be used with this transaction type"


class CategoryNotFound(APIError):
    """
    Category Not Found Exception
    """
    status_code = 404
    code = "NOT_FOUND"
    details = "Category not Found!"


class CategoryNameExists(APIError):
    """
    Category name already Taken Exception
    """
    status_code = 400
    code = "ALREADY_EXISTS"
    details = "This category name already exists!"


class CategoryInvalidType(APIError):
    """
    Invalid Category Type Exception
    """
    status_code = 400
    code = "INVALID_TYPE"
    details = "The informed category type is not valid!"
