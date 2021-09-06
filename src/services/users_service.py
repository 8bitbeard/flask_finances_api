"""
Users Service File
"""

import validators

from werkzeug.security import generate_password_hash

from src.database import db

from src.models.users import User

from src.exceptions.users_exception import UserEmailAlreadyExists, UserEmailInvalid, UserMissingParameter,\
                                          UserNameInvalid, UserPasswordTooShort


class UsersService:
    """
    Users Service Class
    """

    def create(self, data):
        """
        Usee create service method
        """
        if 'email' not in data or 'name' not in data or 'password' not in data:
            raise UserMissingParameter('Email, Username and Password parameters must be provided!')

        name = data['name']
        email = data['email']
        password = data['password']

        if len(name) < 3 or not name.isalnum():
            raise UserNameInvalid(
                'The informed name must be bigger than 3 chars, should be alphanumeric, also no spaces!'
            )

        if not validators.email(email):
            raise UserEmailInvalid('The informed Email is not valid!')

        if User.query.filter_by(email=email).first() is not None:
            raise UserEmailAlreadyExists('The informed Email is already taken!')

        if len(password) < 6:
            raise UserPasswordTooShort('The password must contain 6 or more characters!')

        pwd_hash = generate_password_hash(password)

        user = User(name=name, email=email, password=pwd_hash)

        db.session.add(user)
        db.session.commit()

        return user

    def index(self):
        """
        User list service method
        """

        users = User.query.all()

        return users
