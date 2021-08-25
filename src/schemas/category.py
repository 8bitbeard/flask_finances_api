from marshmallow import fields

from src.database import ma

from src.models.categories import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        fields = ("id", "name", "type")
        ordered = True

    type = fields.Function(lambda obj: obj.type.value)
