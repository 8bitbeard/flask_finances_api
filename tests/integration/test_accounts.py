def test_create_new_account(test_client, init_database, insert_user_db):
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

def test_error_account_with_name_more_than_80_chars(test_client, init_database, insert_user_db):
    login_url = '/api/v1/auth/login'
    login_data = {
        'email': insert_user_db.email,
        'password': 'password'
    }
    login_response = test_client.post(login_url, json=login_data)
    url = '/api/v1/accounts/'
    data = {
        'name': 'Testing Account With name bigger than the allowed wich is at max 80 characters lorem ipsum bla bla bla bla bla bla',
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

def test_error_account_with_name_less_than_3_chars(test_client, init_database, insert_user_db):
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

def test_error_account_with_inexistent_user(test_client, init_database, insert_user_db):
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

def test_error_account_with_invalid_balance(test_client, init_database, insert_user_db):
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

def test_list_user_without_accounts(test_client, init_database, insert_user_db):
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

def test_list_user_with_accounts(test_client, init_database, insert_user_db, insert_account_db):
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

def test_get_account_balance(test_client, init_database, insert_user_db, insert_account_db):
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

def test_error_get_inexistent_account_balance(test_client, init_database, insert_user_db):
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

    print(response)

    assert response.status_code == 404
    assert response.json['code'] == 'NOT_FOUND'
    assert response.json['message'] == 'The given account was not found!'
    assert response.json['details'] == ['The given account was not found!']