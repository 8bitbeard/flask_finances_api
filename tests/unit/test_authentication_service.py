# type: ignore

"""
Test file for users_service.py file
"""


import pytest

from src.models.users import User

from src.services.authentication_service import AuthenticationService

from src.exceptions.users_exception import UserMissingParameter
from src.exceptions.authentication_exceptions import AuthenticationBadCredentials
from src.exceptions.users_exception import UserNotFound

class TestLogin:
    """
    Class for testing the login service method
    """

    def test_login_error_email_missing(self):
        """
        Test if the login method raises a UserMissingParameter exception when no email is given
        """
        with pytest.raises(UserMissingParameter):
            AuthenticationService.login({'password': 'password'})

    def test_login_error_password_missing(self):
        """
        Test if the login method raises a UserMissingParameter exception when no password is given
        """
        with pytest.raises(UserMissingParameter):
            AuthenticationService.login({'email': 'email@example.com'})

    def test_login_error_user_not_found(self, mock_get_sqlalchemy):
        """
        Test if the login method raises a AuthenticationBadCredentials exception when no user is found with
        given credentials
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(AuthenticationBadCredentials):
            AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})

    def test_login_error_bad_password(self, mock_get_sqlalchemy, mock_user_object, mocker):
        """
        Test if the login method raises a AuthenticationBadCredentials exception when password is incorrect
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
        mocker.patch("src.services.authentication_service.check_password_hash").return_value = False
        with pytest.raises(AuthenticationBadCredentials):
            AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})

    def test_login_authentication_service_method(self, mock_get_sqlalchemy, mock_user_object, mock_token_data, mocker):
        """
        Test if the login method returns the login infos successfully
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
        mocker.patch("src.services.authentication_service.check_password_hash").return_value = True
        login = AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})
        assert login['name'] == mock_user_object.name
        assert login['email'] == mock_user_object.email
        assert login['access'] == mock_token_data['access']
        assert login['refresh'] == mock_token_data['refresh']


class TestFind:
    """
    Class for testing the find service method
    """

    def test_find_error_user_not_found(self, mock_get_sqlalchemy):
        """
        Test if the find method raises a UserNotFound when no user is found
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(UserNotFound):
            AuthenticationService.find('user_id')

    def test_find_authentication_service_method(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if the find method returns a user object
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
        user = AuthenticationService.find('user_id')
        assert user.id == mock_user_object.id
        assert user.name == mock_user_object.name
        assert user.email == mock_user_object.email
        assert user.password == mock_user_object.password
