import locale

from marshmallow import fields

from src.database import ma

from src.models.transactions import Transaction

from src.schemas.category import CategorySchema


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True

    category = ma.Nested(CategorySchema)
    value = fields.Function(lambda obj: locale.currency(obj.value))