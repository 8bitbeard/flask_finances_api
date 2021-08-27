import decimal

from src.database import db

from src.models.transactions import Transaction
from src.models.categories import Category, CategoryType
from src.models.accounts import Account

from src.exceptions.categories_exception import CategoryNotFound, IncorrectCategory
from src.exceptions.accounts_exception import AccountNotFound
from src.exceptions.transaction_exception import TransactionValueNegativeOrZero


class TransactionsService:
    def income(user_id, account_id, data):

        value = data['value']
        category_name = data['category']

        if value <= 0:
            raise TransactionValueNegativeOrZero('Transaction values must be bigger than 0!')

        category = Category.query.filter_by(name=category_name, user_id=user_id).first()

        if not category:
            raise CategoryNotFound('Category not found!')

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        if category.type != CategoryType.E:
            raise IncorrectCategory('Category type is S, but must be E!')

        transaction = Transaction(account_id=account_id, value=value, category_id=category.id)

        account.balance += decimal.Decimal(value)
        account.income += decimal.Decimal(value)

        db.session.add(transaction)
        db.session.add(account)
        db.session.commit()

        return transaction



    def expense(user_id, account_id, data):

        value = data['value']
        category_name = data['category']

        if value <= 0:
            raise TransactionValueNegativeOrZero('Transaction values must be bigger than 0!')

        category = Category.query.filter_by(name=category_name, user_id=user_id).first()

        if not category:
            raise CategoryNotFound('Category not found!')

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        if category.type != CategoryType.S:
            raise IncorrectCategory('Category type is E, but must be S!')

        transaction = Transaction(account_id=account_id, value=value, category_id=category.id)

        account.balance -= decimal.Decimal(value)
        account.expense += decimal.Decimal(value)

        db.session.add(transaction)
        db.session.add(account)
        db.session.commit()

        return transaction


    def extract(user_id, account_id):

        account = Account.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            raise AccountNotFound('Account not found!')

        transactions = Transaction.query.filter_by(account_id=account_id)

        return transactions