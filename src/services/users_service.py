import validators

from src.database import db

from src.models.users import User

from src.exceptions.users_exception import UserEmailAlreadyExists, UserEmailInvalid, UserMissingParameter,\
                                          UserNameInvalid


class UsersService:

    def create(data):
        if 'email' not in data or 'name' not in data:
            raise UserMissingParameter('Email and Username parameters must be provided!')

        name = data['name']
        email = data['email']

        if len(name) < 3 or not name.isalnum() or ' ' in name:
            raise UserNameInvalid(
                'The informed name must be bigger than 3 chars, should be alphanumeric, also no spaces!'
            )

        if not validators.email(email):
            raise UserEmailInvalid('The informed Email is not valid!')

        if User.query.filter_by(email=email).first() is not None:
            raise UserEmailAlreadyExists('The informed Email is already taken!')

        user = User(name=name, email=email)

        db.session.add(user)
        db.session.commit()

        return user

    def index():

        users = User.query.all()

        return users
