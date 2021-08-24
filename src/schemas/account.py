import locale

from marshmallow import fields

from src.database import ma

from src.models.accounts import Account


class AccountSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Account
        load_instance = True

    balance = fields.Function(lambda obj: locale.currency(obj.balance))
    income = fields.Function(lambda obj: locale.currency(obj.income))
    expense = fields.Function(lambda obj: locale.currency(obj.expense))
