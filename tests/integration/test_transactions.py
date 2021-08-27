import locale
from datetime import datetime


def test_income_transaction(test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
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

def test_error_income_transaction_with_negative_value(test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
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

def test_error_income_transaction_with_inexistent_category(test_client, init_database, insert_user_db, insert_account_db):
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

def test_error_income_transaction_with_inexistent_account(test_client, init_database, insert_user_db, insert_income_category_db):
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

def test_error_income_transaction_with_expense_category(test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
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

def test_expense_transaction(test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
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

def test_error_expense_transaction_with_negative_value(test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db):
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

def test_error_expense_transaction_with_inexistent_category(test_client, init_database, insert_user_db, insert_account_db):
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

def test_error_expense_transaction_with_inexistent_account(test_client, init_database, insert_user_db, insert_expense_category_db):
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

def test_error_expense_transaction_with_expense_income(test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db):
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

def test_transaction_extract_with_income(test_client, init_database, insert_user_db, insert_account_db, insert_income_category_db, insert_income_transaction_db):
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

def test_transaction_extract_with_expense(test_client, init_database, insert_user_db, insert_account_db, insert_expense_category_db, insert_expense_transaction_db):
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

def test_transaction_extract_without_data(test_client, init_database, insert_user_db, insert_account_db):
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

def test_error_transaction_extract_inexistent_account(test_client, init_database, insert_user_db):
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