import numbers

from src.database import db

from src.models.accounts import Account
from src.models.users import User

from src.exceptions.accounts_exception import AccountNotFound, AccountInvalidName
from src.exceptions.users_exception import UserNotFound
from src.exceptions.balance_exception import BalanceInvalid


class AccountsService:

    def create(user_id, data):
        name = data['name']
        balance = data['balance']

        if 3 > len(name) or len(name) > 80:
            raise AccountInvalidName(
                'The account name must be bigger than 3 and less than 80 chars'
            )

        user = User.query.filter_by(id=user_id).first()

        if not user:
            raise UserNotFound('The user does not exist!')

        if not isinstance(balance, numbers.Number):
            raise BalanceInvalid('Balance value must be numeric!')

        account = Account(user_id=user_id, name=name, balance=balance)

        db.session.add(account)
        db.session.commit()

        return account

    def index(user_id):
        accounts = Account.query.filter_by(user_id=user_id)

        return accounts

    def retrieve(user_id, account_id):

        account = Account.query.filter_by(id=account_id, user_id=user_id).first()

        if account:
            return account
        else:
            raise AccountNotFound('The given account was not found!')