"""
Accounts Service File
"""

import numbers

from src.database import db

from src.models.accounts import Account
from src.models.users import User

from src.exceptions.accounts_exception import AccountNotFound, AccountInvalidName
from src.exceptions.users_exception import UserNotFound
from src.exceptions.balance_exception import BalanceInvalid


class AccountsService:
    """
    Accounts Service Class
    """

    def create(self, user_id, data):
        """
        Create an account service method
        """
        name = data['name']
        balance = data['balance']

        if len(name) < 3 or len(name) > 80:
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

    def index(self, user_id):
        """
        List user accounts service method
        """
        accounts = Account.query.filter_by(user_id=user_id)

        return accounts

    def retrieve(self, user_id, account_id):
        """
        Retrieve user account service method
        """

        account = Account.query.filter_by(id=account_id, user_id=user_id).first()

        if account:
            return account
        raise AccountNotFound('The given account was not found!')
