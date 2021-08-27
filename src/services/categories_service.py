from src.database import db

from src.models.categories import CategoryType, Category
from src.models.users import User

from src.exceptions.categories_exception import CategoryNotFound, CategoryNameExists, CategoryInvalidType
from src.exceptions.users_exception import UserNotFound


class CategoriesService:
    def create(user_id, data):

        name = data['name']
        category_type = data['type']

        is_category_valid = any(category_type == item.name for item in CategoryType)

        if not is_category_valid:
            raise CategoryInvalidType('Informed category is not valid!')

        user = User.query.filter_by(id=user_id).first()

        if not user:
            raise UserNotFound('User not found!')

        is_present = Category.query.filter_by(name=name, user_id=user_id).first()

        if is_present:
            raise CategoryNameExists('There is already a category with the given name!')

        category = Category(name=name, type=category_type, user_id=user_id)

        db.session.add(category)
        db.session.commit()

        return category

    def index(user_id):

        categories = Category.query.filter_by(user_id=user_id)

        return categories
