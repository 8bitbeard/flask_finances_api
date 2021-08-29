import pytest

from src.services.accounts_service import AccountsService

from src.exceptions.accounts_exception import AccountNotFound, AccountInvalidName
from src.exceptions.users_exception import UserNotFound
from src.exceptions.balance_exception import BalanceInvalid

def test_create_error_name_less_than_3_chars():
    with pytest.raises(AccountInvalidName):
        AccountsService.create('id', {'name': 'in', 'balance': 12.25})

def test_create_error_user_not_found(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
    with pytest.raises(UserNotFound):
        AccountsService.create('id', {'name': 'Account', 'balance': 12.25})

def test_create_error_account_balance_invalid(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = True
    with pytest.raises(BalanceInvalid):
        AccountsService.create('id', {'name': 'Account', 'balance': 'invalid'})

def test_create_accounts_service_method(mock_get_sqlalchemy, mock_account_object, mocker):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_account_object
    mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
    account = AccountsService.create('user_id', {'name': 'Account', 'balance': 10.25})
    assert account.id is not None
    assert account.user_id == 'user_id'
    assert account.name == 'Account'
    assert account.balance == 10.25
    assert account.income == 0
    assert account.expense == 0

def test_index_accounts_service_method(mock_get_sqlalchemy, mock_account_object):
    mock_get_sqlalchemy.filter_by.return_value = [mock_account_object]
    accounts = AccountsService.index('user_id')
    assert isinstance(accounts, list)
    assert accounts[0].id is not None
    assert accounts[0].user_id is not None
    assert accounts[0].name == 'Mock Account'
    assert accounts[0].balance == 10.25
    assert accounts[0].income == 0
    assert accounts[0].expense == 0

def test_retrieve_error_account_not_found(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
    with pytest.raises(AccountNotFound):
        AccountsService.retrieve('user_id', 'account_id')

def test_retrieve_accounts_service_method(mock_get_sqlalchemy, mock_account_object):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_account_object
    account = AccountsService.retrieve('user_id', 'account_id')
    assert account.id is not None
    assert account.user_id is not None
    assert account.name == 'Mock Account'
    assert account.balance == 10.25
    assert account.income == 0
    assert account.expense == 0
