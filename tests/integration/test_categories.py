"""
Test file for the authentication routes
"""


class TestCreate:
    """
    Class to test the create blueprint method
    """

    def test_create_new_income_categorie(self, test_client, init_database, insert_user_db):
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        data = {
            'name': 'Testing',
            'type': 'E'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['name'] == 'Testing'
        assert response.json['type'] == 'Entrada'

    def test_create_new_expense_categorie(self, test_client, init_database, insert_user_db):
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        data = {
            'name': 'Testing',
            'type': 'S'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['name'] == 'Testing'
        assert response.json['type'] == 'Saída'

    def test_error_create_category_with_invalid_type(self, test_client, init_database, insert_user_db):
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        data = {
            'name': 'Testing',
            'type': 'INV'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_TYPE'
        assert response.json['message'] == 'Informed category is not valid!'
        assert response.json['details'] == ['The informed category type is not valid!']

    def test_error_create_new_categorie_with_inexistent_user(self, test_client, init_database, insert_user_db):
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)
        init_database.session.delete(insert_user_db)
        init_database.session.commit()

        url = '/api/v1/categories/'
        data = {
            'name': 'Testing',
            'type': 'S'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 404
        assert response.json['code'] == 'NOT_FOUND'
        assert response.json['message'] == 'User not found!'
        assert response.json['details'] == ['User not found!']

    def test_error_create_category_with_existent_name(self, test_client, init_database, insert_user_db,
                                                      insert_income_category_db):
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        data = {
            'name': 'UnitTest',
            'type': 'S'
        }
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.post(url, json=data, headers=headers)

        assert response.status_code == 400
        assert response.json['code'] == 'ALREADY_EXISTS'
        assert response.json['message'] == 'There is already a category with the given name!'
        assert response.json['details'] == ['This category name already exists!']

    def test_error_create_no_authentication_header(self, test_client):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/categories/'
        data = {
            'name': 'UnitTest',
            'type': 'S'
        }
        response = test_client.post(url, json=data)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_create_invalid_authorization_header(self, test_client):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/categories/'
        data = {
            'name': 'UnitTest',
            'type': 'S'
        }
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                             '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
                             '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '
        }
        response = test_client.get(url, json=data, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"


class TestIndex:
    """
    Class to test the index blueprint method
    """

    def test_list_user_without_categories(self, test_client, init_database, insert_user_db):
        """
        Test that an empty list returns when logged in user has no categories
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 0

    def test_list_user_with_categories(self, test_client, init_database, insert_user_db, insert_income_category_db):
        """
        Test that an categories list returns when logged in user has categories
        """
        login_url = '/api/v1/auth/login'
        login_data = {
            'email': insert_user_db.email,
            'password': 'password'
        }
        login_response = test_client.post(login_url, json=login_data)

        url = '/api/v1/categories/'
        headers = {
            'Authorization': 'Bearer {}'.format(login_response.json['access'])
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]['id'] == insert_income_category_db.id
        assert response.json[0]['name'] == insert_income_category_db.name
        assert response.json[0]['type'] == insert_income_category_db.type.value

    def test_error_list_categories_no_authentication_header(self, test_client):
        """
        Test return error when no user exists with bearer token user_id
        """
        url = '/api/v1/categories/'
        response = test_client.get(url)

        assert response.status_code == 401
        assert response.json['msg'] == 'Missing Authorization Header'

    def test_error_list_categories_invalid_authorization_header(self, test_client):
        """
        Test return error when bearer_token is invalid
        """
        url = '/api/v1/categories/'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                             '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
                             '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c '
        }
        response = test_client.get(url, headers=headers)

        assert response.status_code == 422
        assert response.json['msg'] == "Signature verification failed"
