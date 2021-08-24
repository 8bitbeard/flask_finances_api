from src.database import db

from src.models.categories import Category

from src.exceptions.categories_exception import CategoryNotFound, CategoryNameExists


class CategoriesService:
    def create(data):

        name = data['name']
        category_type = data['type']

        is_present = Category.query.filter_by(name=name).first()

        print (is_present)

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
