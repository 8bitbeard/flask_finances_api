# type: ignore

"""
Test file for accounts_service.py file
"""


import pytest

from src.services.accounts_service import AccountsService

from src.exceptions.accounts_exception import AccountNotFound, AccountInvalidName
from src.exceptions.users_exception import UserNotFound
from src.exceptions.balance_exception import BalanceInvalid


class TestCreate:
    """
    Class for testing the create service method
    """

    def test_create_error_name_less_than_3_chars(self):
        """
        Test if create method raises a AccountInvalidName when creating an account with less than 3 chars
        """
        accounts_service = AccountsService()
        with pytest.raises(AccountInvalidName):
            accounts_service.create('id', {'name': 'in', 'balance': 12.25})

    def test_create_error_user_not_found(self, mock_get_sqlalchemy):
        """
        Test if create method raises a UserNotFound when creating an account for an inexistent user
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(UserNotFound):
            accounts_service.create('id', {'name': 'Account', 'balance': 12.25})

    def test_create_error_account_balance_invalid(self, mock_get_sqlalchemy):
        """
        Test if create method raises a BalanceInvalid when creating an account with invalid value
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = True
        with pytest.raises(BalanceInvalid):
            accounts_service.create('id', {'name': 'Account', 'balance': 'invalid'})

    def test_create_accounts_service_method(self, mock_get_sqlalchemy, mock_account_object, mocker):
        """
        Test if create method creates an account successfully
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_account_object
        mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
        account = accounts_service.create(mock_account_object.user_id,
                                         {'name': mock_account_object.name, 'balance': mock_account_object.balance})
        assert account.id is not None
        assert account.user_id == mock_account_object.user_id
        assert account.name == mock_account_object.name
        assert account.balance == mock_account_object.balance
        assert account.income == mock_account_object.income
        assert account.expense == mock_account_object.expense


class TestIndex:
    """
    Class for testing the index service method
    """

    def test_index_accounts_service_method(self, mock_get_sqlalchemy, mock_account_object):
        """
        Test if index method returns a list of accounts
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value = [mock_account_object]
        accounts = accounts_service.index('user_id')
        assert isinstance(accounts, list)
        assert accounts[0].id == mock_account_object.id
        assert accounts[0].user_id  == mock_account_object.user_id
        assert accounts[0].name == mock_account_object.name
        assert accounts[0].balance == mock_account_object.balance
        assert accounts[0].income == mock_account_object.income
        assert accounts[0].expense == mock_account_object.expense


class TestRetrieve:
    """
    Class for testing the retrieve service method
    """

    def test_retrieve_error_account_not_found(self, mock_get_sqlalchemy):
        """
        Test if retrieve method returns an AccountNotFound for an inexistent user
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(AccountNotFound):
            accounts_service.retrieve('user_id', 'account_id')

    def test_retrieve_accounts_service_method(self, mock_get_sqlalchemy, mock_account_object):
        """
        Test if retrieve method returns a account object
        """
        accounts_service = AccountsService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_account_object
        account = accounts_service.retrieve('user_id', 'account_id')
        assert account.id == mock_account_object.id
        assert account.user_id == mock_account_object.user_id
        assert account.name == mock_account_object.name
        assert account.balance == mock_account_object.balance
        assert account.income == mock_account_object.income
        assert account.expense == mock_account_object.expense

