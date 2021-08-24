import numbers

from src.database import db

from src.models.accounts import Account
from src.models.users import User

from src.exceptions.accounts_exception import AccountNotFound
from src.exceptions.users_exception import UserNotFound
from src.exceptions.balance_exception import BalanceInvalid


class AccountsService:

    def create(data):
        user_email = data['email']
        balance = data['balance']

        user = User.query.filter_by(email=user_email).first()

        if not user:
            raise UserNotFound('The user does not exist!')

        if not isinstance(balance, numbers.Number):
            raise BalanceInvalid('Balance value must be numeric!')

        account = Account(user_id=user.id, balance=balance)

        db.session.add(account)
        db.session.commit()

        return account

    def index():
        accounts = Account.query.all()

        return accounts

    def retrieve(account_id):

        account = Account.query.filter_by(id=account_id).first()

        if account:
            return account

        else:
            raise AccountNotFound('The given account was not found!')