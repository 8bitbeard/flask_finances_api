from src.exceptions.base_exception import APIError


class IncorrectCategory(APIError):
    status_code = 400
    code = "INCORRECT_CATEGORY"
    details = "This category cannot be used with this transaction type"


class CategoryNotFound(APIError):
    status_code = 404
    code = "NOT_FOUND"
    details = "Category not Found!"


class CategoryNameExists(APIError):
    status_code = 400
    code = "ALREADY_EXISTS"
    details = "This category name already exists!"