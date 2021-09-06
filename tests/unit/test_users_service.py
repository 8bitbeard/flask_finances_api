# type: ignore

"""
Test file for users_service.py file
"""


import pytest

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
        users_service = UsersService()
        with pytest.raises(UserMissingParameter):
            users_service.create({"email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_without_email(self):
        """
        Test if create method raises a UserMissingParameter exception when no email is informed
        """
        users_service = UsersService()
        with pytest.raises(UserMissingParameter):
            users_service.create({"name":"TestUser", "password": "password"})

    def test_create_error_without_password(self):
        """
        Test if create method raises a UserMissingParameter exception when no password is informed
        """
        users_service = UsersService()
        with pytest.raises(UserMissingParameter):
            users_service.create({"name":"TestUser", "email": "test_user@exmaple.com"})

    def test_create_error_name_less_than_3_chars(self):
        """
        Test if create method raises a UserNameInvalid exception when the name contains less than 3 characters
        """
        users_service = UsersService()
        with pytest.raises(UserNameInvalid):
            users_service.create({"name":"Te", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_name_not_alphanumeric(self):
        """
        Test if create method raises a UserNameInvalid exception when the name contains less than 3 characters
        """
        users_service = UsersService()
        with pytest.raises(UserNameInvalid):
            users_service.create({"name":"T$$%¨e", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_invalid_email(self):
        """
        Test if create method raises a UserEmailInvalid exception when the email is invalid
        """
        users_service = UsersService()
        with pytest.raises(UserEmailInvalid):
            users_service.create({"name":"TestUser", "email": "test_userexmaple.com", "password": "password"})

    def test_create_error_user_already_exists(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if create method raises a UserEmailAlreadyExists exception when the email is already taken
        """
        users_service = UsersService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
        with pytest.raises(UserEmailAlreadyExists):
            users_service.create({"name":"TestUser", "email": "test_user@exmaple.com", "password": "password"})

    def test_create_error_password_too_short(self, mock_get_sqlalchemy):
        """
        Test if create method raises a UserPasswordTooShort exception when the the password contains less than 6 chars
        """
        users_service = UsersService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(UserPasswordTooShort):
            users_service.create({"name":"TestUser", "email": "test_user@exmaple.com", "password": "pass"})

    def test_create_users_service_method(self, mock_get_sqlalchemy, mock_db_session, mock_user_object,
                                         mock_hash_password):
        """
        Test if create method register a new user successfully
        """
        users_service = UsersService()
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        user = users_service.create({"name": mock_user_object.name,
                                    "email": mock_user_object.email, "password": mock_user_object.password})
        assert user.id is not None
        assert user.name == mock_user_object.name
        assert user.email == mock_user_object.email
        assert user.password == mock_hash_password


class TestIndex:
    """
    Class for testing the index service method
    """

    def test_index_users_service_method(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if index method returns a list of users successfully
        """
        users_service = UsersService()
        mock_get_sqlalchemy.all.return_value = [mock_user_object]
        users = users_service.index()
        assert isinstance(users, list)
        assert users[0].id == mock_user_object.id
        assert users[0].name == mock_user_object.name
        assert users[0].email == mock_user_object.email
        assert users[0].password == mock_user_object.password
