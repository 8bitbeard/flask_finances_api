"""
Test file for the account routes
"""


class TestCreateEndpoint:
    """
    Class to test the create endpoint
    """

    def test_create_new_account(self, test_client, init_database, insert_user_db):
        """
        Test creating a new account
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)
        url = '/api/v1/accounts/'
        data = {
            'name': 'Testing Account',
            'balance': 50.25
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 201

    def test_error_no_authorization_header(self, test_client, init_database, insert_user_db):
        """
        Test that the account create endpoint is protected with authentication
        """
        url = '/api/v1/accounts/'
        data = {
            'name': 'Testing Account',
            'balance': 50.25
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['msg'] == "Missing Authorization Header"

    def test_error_invalid_bearer_token(self, test_client, init_database, insert_user_db):
        """
        Test that the account create endpoint fails with invalid bearer token
        """
        url = '/api/v1/accounts/'
        data = {
            'name': 'Testing Account',
            'balance': 50.25
        }
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                             '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
                             '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"

    def test_error_account_with_name_more_than_80_chars(self, test_client, init_database, insert_user_db):
        """
        Test if the endpoint returns an error with account names bigger than 80 chars
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)
        url = '/api/v1/accounts/'
        data = {
            'name': """Testing Account With name bigger than the allowed wich is at max 80\
                    characters lorem ipsum bla bla bla bla bla bla""",
            'balance': 50.25
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_NAME'
        assert response.json['message'] == 'The account name must be bigger than 3 and less than 80 chars'
        assert response.json['details'] == ['The account name must be bigger than 3 and less than 80 chars']

    def test_error_account_with_name_less_than_3_chars(self, test_client, init_database, insert_user_db):
        """
        Test that the endpoint returns an error to accounts with names that contains less than 3 chars
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)
        url = '/api/v1/accounts/'
        data = {
            'name': 'Te',
            'balance': 50.25
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_NAME'
        assert response.json['message'] == 'The account name must be bigger than 3 and less than 80 chars'
        assert response.json['details'] == ['The account name must be bigger than 3 and less than 80 chars']

    def test_error_account_with_inexistent_user(self, test_client, init_database, insert_user_db):
        """
        Test that the endpoint returns an error when creating an account to an inexistent user
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        init_database.session.delete(insert_user_db)
        init_database.session.commit()

        url = '/api/v1/accounts/'
        data = {
            'name': 'Testing Accounts',
            'balance': '50.25'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'The user does not exist!'
        assert response.json['details'] == ['User not found!']

    def test_error_account_with_invalid_balance(self, test_client, init_database, insert_user_db):
        """
        Test that the endpoint returns an error when creating account with invalid balance
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/accounts/'
        data = {
            'name': 'Testing Accounts',
            'balance': 'invalid'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)
        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_BALANCE'
        assert response.json['message'] == 'Balance value must be numeric!'
        assert response.json['details'] == ['Balance value must be numeric!']


class TestIndexEndpoint:
    """
    Class to test the index endpoint /api/v1/accounts GET
    """

    def test_list_user_without_accounts(self, test_client, init_database, insert_user_db):
        """
        Test that the endpoint returns a empty list when user has no accounts
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/accounts/'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 0

    def test_list_user_with_accounts(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test that the endpoint list user accounts
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/accounts/'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]['id'] is not None
        assert response.json[0]['name'] == 'Unit test'
        assert response.json[0]['income'] == 'R$ 0,00'
        assert response.json[0]['expense'] == 'R$ 0,00'
        assert response.json[0]['balance'] == 'R$ 10,25'


class TestBalanceEndpoint:
    """
    Class to test the index endpoint /api/v1/accounts/:accountId/balance GET
    """

    def test_error_list_no_authorization_header(self, test_client, init_database, insert_user_db):
        """
        Test that the account list endpoint is protected with authentication
        """
        url = '/api/v1/accounts/'
        response = test_client.get(url)

        assert response.status_code == 401
        assert response.json['msg'] == "Missing Authorization Header"

    def test_error_list_invalid_bearer_token(self, test_client, init_database, insert_user_db):
        """
        Test that the account list endpoint fails with invalid bearer token
        """
        url = '/api/v1/accounts/'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                             '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
                             '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"

    def test_get_account_balance(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test that the get account balance endpoint returns a valid balance
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/accounts/{}/balance'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)
        assert response.status_code == 200
        assert response.json['balance'] == 'R$ 10,25'

    def test_error_balance_no_authorization_header(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test that the account balance endpoint is protected with authentication
        """
        url = '/api/v1/accounts/{}/balance'.format(insert_account_db.id)
        response = test_client.get(url)

        assert response.status_code == 401
        assert response.json['msg'] == "Missing Authorization Header"

    def test_error_balance_invalid_bearer_token(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test that the account balance endpoint fails with invalid bearer token
        """
        url = '/api/v1/accounts/{}/balance'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                             '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
                             '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"

    def test_error_get_inexistent_account_balance(self, test_client, init_database, insert_user_db):
        """
        Test that the account balance endpoint is protected with authentication
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/accounts/inexistent/balance'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'The given account was not found!'
        assert response.json['details'] == ['The given account was not found!']
