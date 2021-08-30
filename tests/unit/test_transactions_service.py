# type: ignore

"""
Test file for transactions_service.py file
"""


import pytest

from src.services.transactions_service import TransactionsService

from src.exceptions.categories_exception import CategoryNotFound, IncorrectCategory
from src.exceptions.accounts_exception import AccountNotFound
from src.exceptions.transaction_exception import TransactionValueNegativeOrZero


class TestIncome:
    """
    Class for testing the income service method
    """

    def test_income_error_negative_value(self):
        """
        Test if income method raises an TransactionValueNegativeOrZero exception when passing a negative value
        """
        with pytest.raises(TransactionValueNegativeOrZero):
            TransactionsService.income('user_id', 'account_id', {'value': -1, 'category': 'Category'})

    def test_income_error_category_not_fount(self, mock_get_sqlalchemy):
        """
        Test if income method raises an CategoryNotFound exception when no category is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(CategoryNotFound):
            TransactionsService.income('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_income_error_account_not_found(self, mock_get_sqlalchemy, mock_e_category_object):
        """
        Test if income method raises an AccountNotFound exception when no account is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_e_category_object, None]
        with pytest.raises(AccountNotFound):
            TransactionsService.income('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_income_error_account_incorrect_category(self, mock_get_sqlalchemy, mock_s_category_object,
                                                     mock_user_object):
        """
        Test if income method raises an IncorrectCategory exception when an incorrect category is informed
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_s_category_object, mock_user_object]
        with pytest.raises(IncorrectCategory):
            TransactionsService.income('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_income_transactions_service_method(self, mock_get_sqlalchemy, mock_account_object, mock_e_category_object,
                                                mocker):
        """
        Test if income method creates a income transaction successfully
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_e_category_object, mock_account_object]
        mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
        transaction = TransactionsService.income('user_id', 'account_id', {'value': 1, 'category': 'Category'})

        assert transaction.id is not None
        assert transaction.account_id is not None
        assert transaction.value == 1
        assert transaction.category_id == mock_e_category_object.id
        assert transaction.created_at is not None


class TestExpense:
    """
    Class for testing the expense service method
    """

    def test_expense_error_negative_value(self):
        """
        Test if expense method raises an TransactionValueNegativeOrZero exception when passing a negative value
        """
        with pytest.raises(TransactionValueNegativeOrZero):
            TransactionsService.expense('user_id', 'account_id', {'value': -1, 'category': 'Category'})

    def test_expense_error_category_not_fount(self, mock_get_sqlalchemy):
        """
        Test if expense method raises an CategoryNotFound exception when no category is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(CategoryNotFound):
            TransactionsService.expense('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_expense_error_account_not_found(self, mock_get_sqlalchemy, mock_s_category_object):
        """
        Test if expense method raises an AccountNotFound exception when no account is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_s_category_object, None]
        with pytest.raises(AccountNotFound):
            TransactionsService.expense('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_expense_error_account_incorrect_category(self, mock_get_sqlalchemy, mock_e_category_object,
                                                      mock_user_object):
        """
        Test if expense method raises an IncorrectCategory exception when an incorrect category is informed
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_e_category_object, mock_user_object]
        with pytest.raises(IncorrectCategory):
            TransactionsService.expense('user_id', 'account_id', {'value': 1, 'category': 'Category'})

    def test_expense_transactions_service_method(self, mock_get_sqlalchemy, mock_account_object, mock_s_category_object,
                                                mocker):
        """
        Test if expense method creates a income transaction successfully
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_s_category_object, mock_account_object]
        mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
        transaction = TransactionsService.expense('user_id', 'account_id', {'value': 1, 'category': 'Category'})

        assert transaction.id is not None
        assert transaction.account_id is not None
        assert transaction.value == 1
        assert transaction.category_id == mock_s_category_object.id
        assert transaction.created_at is not None


class TestExtract:
    """
    Class for testing the extract service method
    """

    def test_extract_error_account_not_found(self, mock_get_sqlalchemy):
        """
        Test if extract method raises an AccountNotFound exception when no account is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(AccountNotFound):
            TransactionsService.extract('user_id', 'account_id')

    def test_extract_transactions_service_method(self, mock_get_sqlalchemy, mock_account_object, mock_transaction_object,
                                                mocker):
        """
        Test if extract method returns the transactions extract of a given account
        """
        mocked_first = mocker.Mock()
        mocked_first.first = mocker.Mock(return_value = mock_account_object)
        mock_get_sqlalchemy.filter_by.side_effect = [mocked_first, [mock_transaction_object]]
        extract = TransactionsService.extract('user_id', 'account_id')
        assert isinstance(extract, list)
        assert extract[0].id == mock_transaction_object.id
        assert extract[0].account_id == mock_transaction_object.account_id
        assert extract[0].value == mock_transaction_object.value
        assert extract[0].category_id == mock_transaction_object.category_id
        assert extract[0].created_at == mock_transaction_object.created_at
