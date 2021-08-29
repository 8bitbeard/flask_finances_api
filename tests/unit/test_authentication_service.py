import pytest

from src.models.users import User

from src.services.authentication_service import AuthenticationService

from src.exceptions.users_exception import UserMissingParameter
from src.exceptions.authentication_exceptions import AuthenticationBadCredentials
from src.exceptions.users_exception import UserNotFound

def test_login_error_email_missing():
    with pytest.raises(UserMissingParameter):
        AuthenticationService.login({'password': 'password'})

def test_login_error_password_missing():
    with pytest.raises(UserMissingParameter):
        AuthenticationService.login({'email': 'email@example.com'})

def test_login_error_user_not_found(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
    with pytest.raises(AuthenticationBadCredentials):
        AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})

def test_login_error_bad_password(mock_get_sqlalchemy, mock_user_object, mocker):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
    mocker.patch("src.services.authentication_service.check_password_hash").return_value = False
    with pytest.raises(AuthenticationBadCredentials):
        AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})

def test_login_authentication_service_method(mock_get_sqlalchemy, mock_user_object, mocker):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
    mocker.patch("src.services.authentication_service.check_password_hash").return_value = True
    mocker.patch("src.services.authentication_service.create_access_token").return_value = 'access_token'
    mocker.patch("src.services.authentication_service.create_refresh_token").return_value = 'refresh_token'
    login = AuthenticationService.login({'email': 'email@example.com', 'password': 'password'})
    assert login['name'] == mock_user_object.name
    assert login['email'] == mock_user_object.email
    assert login['access'] == 'access_token'
    assert login['refresh'] == 'refresh_token'

def test_find_error_user_not_found(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
    with pytest.raises(UserNotFound):
        AuthenticationService.find('user_id')

def test_find_authentication_service_method(mock_get_sqlalchemy, mock_user_object):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = mock_user_object
    user = AuthenticationService.find('user_id')
    assert user.id == mock_user_object.id
    assert user.name == mock_user_object.name
    assert user.email == mock_user_object.email
    assert user.password == mock_user_object.password