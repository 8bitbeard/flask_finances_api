"""
Users routes tests
"""


class TestCreate:
    """
    Class to test create blueprint method
    """

    def test_register_new_user(self, test_client, init_database):
        """
        Test the creation of a new user
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTester',
            'email': 'func_teste@example.com',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 201
        assert response.json['id'] is not None
        assert response.json['name'] == data['name']
        assert response.json['email'] == data['email']

    def test_error_register_user_without_name(self, test_client, init_database):
        """
        Test the error when trying to register a user without passing the name variable
        """
        url = '/api/v1/users/'
        data = {
            'email': 'func_teste@example.com',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'MISSING_PARAMETER'
        assert response.json['message'] == 'Email, Username and Password parameters must be provided!'
        assert response.json['details'] == ['Missing mandatory parameters!']

    def test_error_register_user_without_email(self, test_client, init_database):
        """
        Test the error when trying to register a user without passing the email variable
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTest',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'MISSING_PARAMETER'
        assert response.json['message'] == 'Email, Username and Password parameters must be provided!'
        assert response.json['details'] == ['Missing mandatory parameters!']

    def test_error_register_user_without_password(self, test_client, init_database):
        """
        Test the error when trying to register a user without passing the password variable
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTest',
            'email': 'func_teste@example.com',
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'MISSING_PARAMETER'
        assert response.json['message'] == 'Email, Username and Password parameters must be provided!'
        assert response.json['details'] == ['Missing mandatory parameters!']

    def test_error_register_user_with_invalid_name(self, test_client, init_database):
        """
        Test the error when trying to register a user with invalid name
        """
        url = '/api/v1/users/'
        data = {
            'name': 'Func Test@',
            'email': 'func_teste@example.com',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_NAME'
        assert response.json['message'] == \
               'The informed name must be bigger than 3 chars, should be alphanumeric, also no spaces!'
        assert response.json['details'] == ['Provided name is invalid!']

    def test_error_register_user_with_invalid_email(self, test_client, init_database):
        """
        Test the error when trying to register a user with invalid email
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTest',
            'email': 'func_testeexample.com',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_EMAIL'
        assert response.json['message'] == 'The informed Email is not valid!'
        assert response.json['details'] == ['Provided email is invalid!']

    def test_error_register_user_with_taken_email(self, test_client, init_database, insert_user_db):
        """
        Test the error when trying to register a user with an already used email
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTest',
            'email': 'mock_user@example.com',
            'password': 'password'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 409
        assert response.json['code'] == 'EMAIL_ALREADY_EXISTS'
        assert response.json['message'] == 'The informed Email is already taken!'
        assert response.json['details'] == ['This email is already taken!']

    def test_error_register_user_with_short_password(self, test_client, init_database):
        """
        Test the error when trying to register a user with a short password
        """
        url = '/api/v1/users/'
        data = {
            'name': 'FuncTest',
            'email': 'func_teste@example.com',
            'password': 'pass'
        }
        response = test_client.post(url, json=data)
        assert response.status_code == 400
        assert response.json['code'] == 'INVALID_PASSWORD'
        assert response.json['message'] == 'The password must contain 6 or more characters!'
        assert response.json['details'] == ['Provided password is invalid!']


class TestIndex:
    """
    Class to test create blueprint method
    """

    def test_list_users(self, test_client, init_database, insert_user_db):
        """
        Test the list users route
        """
        url = '/api/v1/users/'
        response = test_client.get(url)
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]['id'] == insert_user_db.id
        assert response.json[0]['name'] == insert_user_db.name
        assert response.json[0]['email'] == insert_user_db.email
