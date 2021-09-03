"""
Balance Schema File
"""

import locale

from marshmallow import fields

from src.database import ma

from src.models.accounts import Account


class BalanceSchema(ma.SQLAlchemyAutoSchema):
    """
    Balance Schema Class
    """
    class Meta:
        """
        Meta Class
        """
        model = Account
        load_instance = True
        fields = ("balance",)

    balance = fields.Function(lambda obj: locale.currency(obj.balance))
