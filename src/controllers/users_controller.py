"""
Users Controller File
"""

from flask import Blueprint, request

from src.constants import http_status_codes

from src.services.users_service import UsersService

from src.schemas.user import UserSchema


users = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users.post('/')
def create():
    """
    Create a new user
    """
    data = request.json

    users_service = UsersService()
    user_schema = UserSchema()

    found_user = users_service.create(data)

    return user_schema.jsonify(found_user), http_status_codes.HTTP_201_CREATED


@users.get('/')
def index():
    """
    List all created users
    """
    users_service = UsersService()
    user_schema = UserSchema(many=True)

    found_users = users_service.index()

    return user_schema.jsonify(found_users), http_status_codes.HTTP_200_OK
