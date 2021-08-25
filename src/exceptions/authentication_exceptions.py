from src.exceptions.base_exception import APIError


class AuthenticationBadCredentials(APIError):
    status_code = 401
    code = "UNAUTHORIZED"
    details = "Wrong credentials!"