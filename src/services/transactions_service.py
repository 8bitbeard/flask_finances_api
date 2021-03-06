"""
Transactions Service File
"""

import decimal

from src.database import db

from src.models.transactions import Transaction
from src.models.categories import Category, CategoryType
from src.models.accounts import Account

from src.exceptions.categories_exception import CategoryNotFound, IncorrectCategory
from src.exceptions.accounts_exception import AccountNotFound
from src.exceptions.transaction_exception import TransactionValueNegativeOrZero


class TransactionsService:
    """
    Transactions Servie Class
    """
    def income(self, user_id, account_id, data):
        """
        Transaction income service method
        """

        value = data['value']
        category_name = data['category']

        if value <= 0:
            raise TransactionValueNegativeOrZero('Transaction values must be bigger than 0!')

        category = Category.query.filter_by(name=category_name, user_id=user_id).first()

        if not category:
            raise CategoryNotFound('Category not found!')

        if category.type != CategoryType.E:
            raise IncorrectCategory('Category type is S, but must be E!')

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        transaction = Transaction(account_id=account_id, value=value, category_id=category.id)

        account.balance += decimal.Decimal(value)
        account.income += decimal.Decimal(value)

        db.session.add(transaction)
        db.session.add(account)
        db.session.commit()

        return transaction

    def expense(self, user_id, account_id, data):
        """
        Transaction expense service method
        """

        value = data['value']
        category_name = data['category']

        if value <= 0:
            raise TransactionValueNegativeOrZero('Transaction values must be bigger than 0!')

        category = Category.query.filter_by(name=category_name, user_id=user_id).first()

        if not category:
            raise CategoryNotFound('Category not found!')

        if category.type != CategoryType.S:
            raise IncorrectCategory('Category type is E, but must be S!')

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        transaction = Transaction(account_id=account_id, value=value, category_id=category.id)

        account.balance -= decimal.Decimal(value)
        account.expense += decimal.Decimal(value)

        db.session.add(transaction)
        db.session.add(account)
        db.session.commit()

        return transaction

    def extract(self, user_id, account_id):
        """
        Transaction extract service method
        """

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        transactions = Transaction.query.filter_by(account_id=account_id)

        return transactions
