"""
Test file for the authentication routes
"""


class TestCreate:
    """
    Class to test login blueprint method
    """

    def test_login_with_valid_user(self, test_client, init_database, insert_user_db):
        """
        Test login with valid user data
        """
        url = '/api/v1/auth/login'
        data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 201
        assert response.json['name'] == insert_user_db.name
        assert response.json['email'] == insert_user_db.email
        assert response.json['access'] != None
        assert response.json['refresh'] != None

    def test_error_login_without_email(self, test_client, init_database, insert_user_db):
        """
        Test login error when no email is informed
        """
        url = '/api/v1/auth/login'
        data = {
            'password': 'password'
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 400
        assert response.json['code'] == 'MISSING_PARAMETER'
        assert response.json['message'] == 'Email and Password parameters must be provided!'
        assert response.json['details'] == ['Missing mandatory parameters!']

    def test_error_login_without_password(self, test_client, init_database, insert_user_db):
        """
        Test login error when no password is informed
        """
        url = '/api/v1/auth/login'
        data = {
            'email': insert_user_db.email,
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 400
        assert response.json['code'] == 'MISSING_PARAMETER'
        assert response.json['message'] == 'Email and Password parameters must be provided!'
        assert response.json['details'] == ['Missing mandatory parameters!']

    def test_error_login_with_invalid_email(self, test_client, init_database, insert_user_db):
        """
        Test login error when an invalid/inexistent email is informed
        """
        url = '/api/v1/auth/login'
        data = {
            'email': 'invalid',
            'password': 'password'
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['code'] == 'UNAUTHORIZED'
        assert response.json['message'] == 'Email or password invalid!'
        assert response.json['details'] == ['Wrong credentials!']

    def test_error_login_with_invalid_password(self, test_client, init_database, insert_user_db):
        """
        Test login error when an invalid password is informed
        """
        url = '/api/v1/auth/login'
        data = {
            'email': insert_user_db.email,
            'password': 'word'
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['code'] == 'UNAUTHORIZED'
        assert response.json['message'] == 'Email or password invalid!'
        assert response.json['details'] == ['Wrong credentials!']


class TestFind:
    """
    Class to test find blueprint method
    """

    def test_logged_user_data(self, test_client, init_database, insert_user_db):
        """
        Test retrieve logged user data
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/auth/me'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert response.json['id'] != None
        assert response.json['name'] == insert_user_db.name
        assert response.json['email'] == insert_user_db.email

    def test_error_inexistent_user_data(self, test_client, init_database, insert_user_db):
        """
        Test return error when no user exists with bearer token user_id
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)
        init_database.session.delete(insert_user_db)
        init_database.session.commit()

        url = '/api/v1/auth/me'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'User not found!'
        assert response.json['details'] == ['User not found!']

    def test_error_find_no_authentication_header(self, test_client):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/auth/me'
        response = test_client.get(url)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_find_invalid_authorization_header(self, test_client):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/auth/me'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"
