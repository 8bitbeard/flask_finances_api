from marshmallow import fields

from src.database import ma

from src.models.categories import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

    type = fields.Method("type_dict")

    def type_dict(self, obj):
        types = {
            'E': 'Entrada',
            'S': 'Saída'
        }

        return types[obj.type]