"""
Authorization Controller File
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants import http_status_codes

from src.services.authentication_service import AuthenticationService

from src.schemas.user import UserSchema


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/login')
def create():
    """
    Login user controller method
    """
    data = request.json

    token = AuthenticationService.login(data)

    return jsonify(token), http_status_codes.HTTP_201_CREATED

@auth.get('/me')
@jwt_required()
def find():
    """
    Get logged in user data
    """
    user_id = get_jwt_identity()

    user = AuthenticationService.find(user_id)

    user_schema = UserSchema()

    return user_schema.jsonify(user), http_status_codes.HTTP_200_OK
