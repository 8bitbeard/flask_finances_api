def test_login_with_valid_user(test_client, init_database, insert_user_db):
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

def test_error_login_without_email(test_client, init_database, insert_user_db):
    url = '/api/v1/auth/login'
    data = {
        'password': 'password'
    }
    response = test_client.post(url, json=data)

    assert response.status_code == 400
    assert response.json['code'] == 'MISSING_PARAMETER'
    assert response.json['message'] == 'Email and Password parameters must be provided!'
    assert response.json['details'] == ['Missing mandatory parameters!']

def test_error_login_without_password(test_client, init_database, insert_user_db):
    url = '/api/v1/auth/login'
    data = {
        'email': insert_user_db.email,
    }
    response = test_client.post(url, json=data)

    assert response.status_code == 400
    assert response.json['code'] == 'MISSING_PARAMETER'
    assert response.json['message'] == 'Email and Password parameters must be provided!'
    assert response.json['details'] == ['Missing mandatory parameters!']

def test_error_login_with_invalid_email(test_client, init_database, insert_user_db):
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

def test_error_login_with_invalid_password(test_client, init_database, insert_user_db):
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

def test_logged_user_data(test_client, init_database, insert_user_db):
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

def test_error_inexistent_user_data(test_client, init_database, insert_user_db):
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
