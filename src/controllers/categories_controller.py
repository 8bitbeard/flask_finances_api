from flask import Blueprint, request

from src.services.categories_service import CategoriesService

from src.constants import http_status_codes

from src.schemas.category import CategorySchema


categories = Blueprint("categories", __name__, url_prefix="/api/v1/categories")


@categories.post('/')
def create():
    data = request.json

    category_schema = CategorySchema()

    found_category = CategoriesService.create(data)

    return category_schema.jsonify(found_category), http_status_codes.HTTP_201_CREATED


@categories.get('/')
def index():

    category_schema = CategorySchema(many=True)

    found_categories = CategoriesService.index()

    return category_schema.jsonify(found_categories), http_status_codes.HTTP_200_OK


