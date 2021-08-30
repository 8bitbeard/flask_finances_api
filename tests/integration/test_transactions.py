"""
Test file for the transactions routes
"""

import locale


class TestIncome:
    """
    Class to test the income blueprint method
    """

    def test_income_transaction(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
        """
        Test if expense transaction is created sucessfully
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_income_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['value'] == 'R$ 1,25'
        assert response.json['created_at'] is not None
        assert response.json['category']['id'] is not None
        assert response.json['category']['name'] == insert_income_category_db.name
        assert response.json['category']['type'] == 'Entrada'

    def test_error_income_transaction_with_negative_value(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
        """
        Test error when transaction is created with negative value
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': -1.25,
            'category': insert_income_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_VALUE'
        assert response.json['message'] == 'Transaction values must be bigger than 0!'
        assert response.json['details'] == ['Transaction values must be bigger than 0!']

    def test_error_income_transaction_with_inexistent_category(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test error when transaction is created with inexistent category
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': 'inexistent'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'Category not found!'
        assert response.json['details'] == ['Category not Found!']

    def test_error_income_transaction_with_inexistent_account(self, test_client, init_database, insert_user_db, insert_income_category_db):
        """
        Test error when transaction is created with inexistent category
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/inexistent/income'
        data = {
            'value': 1.25,
            'category': insert_income_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'Account not found!'
        assert response.json['details'] == ['The given account was not found!']

    def test_error_income_transaction_with_expense_category(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test error when transaction is created with incorrect category type
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_expense_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INCORRECT_CATEGORY'
        assert response.json['message'] == 'Category type is S, but must be E!'
        assert response.json['details'] == ['This category cannot be used with this transaction type']

    def test_error_income_transaction_no_authentication_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_income_category_db.name
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_income_transaction_invalid_authorization_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/transactions/{}/income'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_income_category_db.name
        }
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"


class TestExpense:
    """
    Class to test the expense blueprint method
    """

    def test_expense_transaction(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test if expense transaction is created sucessfully
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_expense_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['value'] == 'R$ 1,25'
        assert response.json['created_at'] is not None
        assert response.json['category']['id'] is not None
        assert response.json['category']['name'] == insert_expense_category_db.name
        assert response.json['category']['type'] == 'Saída'

    def test_error_expense_transaction_with_negative_value(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test error when transaction is created with negative value
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': -1.25,
            'category': insert_expense_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_VALUE'
        assert response.json['message'] == 'Transaction values must be bigger than 0!'
        assert response.json['details'] == ['Transaction values must be bigger than 0!']

    def test_error_expense_transaction_with_inexistent_category(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test error when transaction is created with inexistent category
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': 'inexistent'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'Category not found!'
        assert response.json['details'] == ['Category not Found!']

    def test_error_expense_transaction_with_inexistent_account(self, test_client, init_database, insert_user_db, insert_expense_category_db):
        """
        Test error when transaction is created with inexistent account
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/inexistent/expense'
        data = {
            'value': 1.25,
            'category': insert_expense_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'Account not found!'
        assert response.json['details'] == ['The given account was not found!']

    def test_error_expense_transaction_with_income_category(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
        """
        Test error when transaction is created with incorrect category type
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_income_category_db.name
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INCORRECT_CATEGORY'
        assert response.json['message'] == 'Category type is E, but must be S!'
        assert response.json['details'] == ['This category cannot be used with this transaction type']

    def test_error_expense_transaction_no_authentication_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_expense_category_db.name
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_expense_transaction_invalid_authorization_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/transactions/{}/expense'.format(insert_account_db.id)
        data = {
            'value': 1.25,
            'category': insert_expense_category_db.name
        }
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"


class TestExtract:
    """
    Class to test the extract blueprint method
    """

    def test_transaction_extract_with_income(self, test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db, insert_income_transaction_db):
        """
        Test if extract displays income transactions correctly
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/extract'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]['id'] == insert_income_transaction_db.id
        assert response.json[0]['value'] == locale.currency(insert_income_transaction_db.value)
        assert response.json[0]['created_at'] == insert_income_transaction_db.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert response.json[0]['category']['id'] == insert_income_category_db.id
        assert response.json[0]['category']['name'] == insert_income_category_db.name
        assert response.json[0]['category']['type'] == 'Entrada'

    def test_transaction_extract_with_expense(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db, insert_expense_transaction_db):
        """
        Test if extract displays expense transactions correctly
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/extract'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]['id'] == insert_expense_transaction_db.id
        assert response.json[0]['value'] == locale.currency(insert_expense_transaction_db.value)
        assert response.json[0]['created_at'] == insert_expense_transaction_db.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        assert response.json[0]['category']['id'] == insert_expense_category_db.id
        assert response.json[0]['category']['name'] == insert_expense_category_db.name
        assert response.json[0]['category']['type'] == 'Saída'

    def test_transaction_extract_without_data(self, test_client, init_database, insert_user_db, insert_account_db):
        """
        Test if extract displays empty list when there is no transactions
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/{}/extract'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 0

    def test_error_transaction_extract_inexistent_account(self, test_client, init_database, insert_user_db):
        """
        Test if returns an error when informed account does not exists
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/transactions/inexistent/extract'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'Account not found!'
        assert response.json['details'] == ['The given account was not found!']

    def test_error_transaction_extract_no_authentication_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/transactions/{}/extract'.format(insert_account_db.id)
        response = test_client.get(url)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_transaction_extract_invalid_authorization_header(self, test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/transactions/{}/extract'.format(insert_account_db.id)
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"
