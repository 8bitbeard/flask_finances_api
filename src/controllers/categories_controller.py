from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.categories_service import CategoriesService

from src.constants import http_status_codes

from src.schemas.category import CategorySchema


categories = Blueprint("categories", __name__, url_prefix="/api/v1/categories")


@categories.post('/')
@jwt_required()
def create():
    data = request.json
    user_id = get_jwt_identity()

    category_schema = CategorySchema()

    found_category = CategoriesService.create(user_id, data)

    return category_schema.jsonify(found_category), http_status_codes.HTTP_201_CREATED


@categories.get('/')
@jwt_required()
def index():
    user_id = get_jwt_identity()

    category_schema = CategorySchema(many=True)

    found_categories = CategoriesService.index(user_id)

    return category_schema.jsonify(found_categories), http_status_codes.HTTP_200_OK


