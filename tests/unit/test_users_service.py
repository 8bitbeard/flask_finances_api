"""
Test file for users_service.py file
"""


import pytest

from src.database import db

from src.exceptions.users_exception import UserMissingParameter, UserNameInvalid, UserEmailInvalid, UserEmailAlreadyExists, UserPasswordTooShort
from src.services.users_service import UsersService


class TestCreate:
    """
    Class for testing the create service method
    """

    def test_create_error_without_name(self):
        """
        Test if create method raises a UserMissingParameter exception when no name is informed
        """
        with pytest.raises(UserMissingParameter):
            UsersService.create({"email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_without_email(self):
        """
        Test if create method raises a UserMissingParameter exception when no email is informed
        """
        with pytest.raises(UserMissingParameter):
            UsersService.create({"name":"TestUser", "password": "password"})

    def test_create_error_without_password(self):
        """
        Test if create method raises a UserMissingParameter exception when no password is informed
        """
        with pytest.raises(UserMissingParameter):
            UsersService.create({"name":"TestUser", "email": "test_user@exmaple.com"})

    def test_create_error_name_less_than_3_chars(self):
        """
        Test if create method raises a UserNameInvalid exception when the name contains less than 3 characters
        """
        with pytest.raises(UserNameInvalid):
            UsersService.create({"name":"Te", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_name_not_alphanumeric(self):
        """
        Test if create method raises a UserNameInvalid exception when the name contains less than 3 characters
        """
        with pytest.raises(UserNameInvalid):
            UsersService.create({"name":"T$$%¨e", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_invalid_email(self):
        """
        Test if create method raises a UserEmailInvalid exception when the email is invalid
        """
        with pytest.raises(UserEmailInvalid):
            UsersService.create({"name":"TestUser", "email": "test_userexmaple.com", "password": "password"})

    def test_create_error_user_already_exists(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if create method raises a UserEmailAlreadyExists exception when the email is already taken
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
        with pytest.raises(UserEmailAlreadyExists):
            UsersService.create({"name":"TestUser", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_password_too_short(self, mock_get_sqlalchemy):
        """
        Test if create method raises a UserPasswordTooShort exception when the the password contains less than 6 chars
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(UserPasswordTooShort):
            UsersService.create({"name":"TestUser", "email": "test_user@exmaple.com", "password": "pass"})

    def test_create_users_service_method(self, mock_get_sqlalchemy, mocker):
        """
        Test if create method register a new user successfully
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        mocker.patch("src.services.users_service.generate_password_hash").return_value = 'hashed_password'
        mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
        user = UsersService.create({"name":"TestUser", "email": "test_user@example.com", "password": "password"})
        assert user.id is not None
        assert user.name == 'TestUser'
        assert user.email == 'test_user@example.com'
        assert user.password == 'hashed_password'


class TestIndex:
    """
    Class for testing the index service method
    """

    def test_index_users_service_method(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if index method returns a list of users successfully
        """
        mock_get_sqlalchemy.all.return_value = [mock_user_object]
        users = UsersService.index()
        assert isinstance(users, list)
        assert users[0].id is not None
        assert users[0].name == 'Mock User'
        assert users[0].email == 'mock_user@example.com'
        assert users[0].password == 'password'
