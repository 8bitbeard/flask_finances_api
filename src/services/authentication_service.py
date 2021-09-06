"""
Authentication Service File
"""

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.users import User

from src.exceptions.users_exception import UserMissingParameter
from src.exceptions.authentication_exceptions import AuthenticationBadCredentials
from src.exceptions.users_exception import UserNotFound


class AuthenticationService:
    """
    Authentication Service Class
    """

    def login(self, data):
        """
        Login service method
        """
        if 'email' not in data or 'password' not in data:
            raise UserMissingParameter('Email and Password parameters must be provided!')

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user:
            is_pass_correct = check_password_hash(user.password, password)

            if is_pass_correct:
                return {
                    "name": user.name,
                    "email": user.email,
                    "access": create_access_token(identity=user.id),
                    "refresh": create_refresh_token(identity=user.id)
                }
        raise AuthenticationBadCredentials('Email or password invalid!')

    def find(self, user_id):
        """
        Find user data service method
        """
        user = User.query.filter_by(id=user_id).first()

        if not user:
            raise UserNotFound('User not found!')

        return user
