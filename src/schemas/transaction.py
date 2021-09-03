"""
Transaction Schema File
"""

import locale

from marshmallow import fields

from src.database import ma

from src.models.transactions import Transaction

from src.schemas.category import CategorySchema


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    """
    Transaction Schema Class
    """
    class Meta:
        """
        Meta Class
        """
        model = Transaction
        load_instance = True
        fields = ("id", "value", "created_at", "category")
        ordered = True

    category = ma.Nested(CategorySchema)
    value = fields.Function(lambda obj: locale.currency(obj.value))
