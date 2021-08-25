from src.database import db

from src.models.categories import CategoryType, Category

from src.exceptions.categories_exception import CategoryNotFound, CategoryNameExists, CategoryInvalidType


class CategoriesService:
    def create(data):

        name = data['name']
        category_type = data['type']

        is_category_valid = any(category_type == item.name for item in CategoryType)

        if not is_category_valid:
            raise CategoryInvalidType('Informed category is not valid!')

        is_present = Category.query.filter_by(name=name).first()

        if is_present:
            raise CategoryNameExists('There is already a category with the given name!')

        category = Category(name=name, type=category_type)

        db.session.add(category)
        db.session.commit()

        return category

    def index():

        categories = Category.query.all()

        return categories

    def retrieve(category_name):

        category = Category.query.filter_by(name=category_name).first()

        if category:
            return category
        else:
            raise CategoryNotFound('Category not Found!')
