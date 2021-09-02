# Flask Finances API

A simple finances API made with Flask and SQLAlchemy. The API documentation is hosted on Github Pages, and can be acessed on the link: https://8bitbeard.github.io/flask_finances_api/


# Techs used
- Flask
- SQLAlchemy
- Marshmallow
- PostgreSQL
- Pytest
- Docker Compose

# Installing the Development Environment
## If you have Docker Compose on your machine

- Clone this repository on your machine
- cd into the repository folder, and build the docker images with docker-compose:
```bash
$ cd flask_finances_api

$ docker-compose up -d -build
```

Since this project uses locale currency to convert monetary values accordingly to the locale, and since python-apline does not support locales natively, the app image was built with ubuntu:latest.

After building the images, if no errors are displayed, you should see something like this on your shell:

```bash
Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
Creating flask_finances_api_db_1 ... done
Creating flask_finances_api_api_1 ... done

```

And if you run the command `docker-compose ps` you should get the following return

```bash
$ docker-compose ps
          Name                        Command              State                    Ports
-----------------------------------------------------------------------------------------------------------
flask_finances_api_api_1   sh ./docker-entrypoint.sh       Up      0.0.0.0:5000->5000/tcp,:::5000->5000/tcp
flask_finances_api_db_1    docker-entrypoint.sh postgres   Up      5432/tcp

```


## If you don't have Docker Compose on your machine
- Install python3 on your machine. You can download it on the following link: https://www.python.org/downloads/
- install virtualenv package with pip:
```bash
$ pip install virtualenv
```
- Clone this repository on your machine
- cd into the repository folder, and create a python virtual environment:
```bash
$ cd flask_finances_api

$ virtualenv venv
```
- Activate your new python virtual environment:
```bash
# Windows OS
$ .\venv\Script\activate.bat

# Unix OS
$ source /venv/bin/activate

```
- Install all the python packages from the requirements.txt file
```bash
$(venv) pip install -r requirements.txt
```

# Configuring the envionment variables
- To run the Flask application, you will need to create a `.env` (or a `.env.docker` if you followed the Docker Compose way) file on the root of the project with the following variables:
```
export FLASK_APP=src
export FLASK_ENV=development
export SECRET_KEY=<define_a_secretkey_here>
export JWT_SECRET_KEY=<define_a_jwt_secretkey_here>
export DATABASE_URL=<define_a_development_database_url_here> # this should be postgresql://postgres:postgres@db:5432/flask_finances_development if running with docker compose
export DATABASE_URL_TST=<define_a_testing_database_url_here>
```

# Configuring the database
This project needs a Relational Database, like PostgreSQL or MySQL. You can choose the one you like the most. After creating it, you will need to add the url on the `DATABASE_URL` environment variable.

After that, run the following commands:
```bash
$(venv) flask db migrate

$(venv) flask db upgrade
```

Atention: If you want to run the **integration** tests on your machine, you will need to create a second database, and add the url on the `DATABASE_URL_TST` environment variable.

The testing db will be configured with the pytest fixture, so there is no need to run migrations on it

# Starting the Local Server
To start the local server, run the following command:
```bash
$(venv) flask run
```

This will start the server on the port 5000 (url: http://localhost:5000).

# Using the API

### You can see all the listed endpoints on the

First you will need to create a new user, so call the **POST** endpoint **/api/v1/auth/users/** with the following body (As an example):
```json
{
	"name": "Example User",
	"email": "example_user@xample.com",
	"password": "example"
}
```
After that you will have a registered user. You can call the **GET** endpoint **/api/v1/auth/users/** and confirm that:
```json
[
  {
    "id": "3019c1a4-6388-4bbb-a121-59017027ca17",
    "name": "Example User",
    "email": "example_user@example.com"
  }
]
```

With the registered user, you can now login on the application, to make request to the other endpoints. Make an request to the **POST** endpoint **/api/v1/auth/login**, and log in:
```json
[
  {
    "email": "example_user@example.com",
    "password": "example"
  }
]
```

This will give you a valid access_token!
```json
{
  "name": "Example User",
  "email": "example_user@example.com",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMDQyNDc5NiwianRpIjoiOGJlMGQ4NDktMDU4NC00ZWExLWFiMTctMzJkYjRmZWQ5Njc0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjMwMTljMWE0LTYzODgtNGJiYi1hMTIxLTU5MDE3MDI3Y2ExNyIsIm5iZiI6MTYzMDQyNDc5NiwiZXhwIjoxNjMwNDI1Njk2fQ.JeDXbcvu4a63UMJ1BzZPTgxMIcflNmF4nP9zNOU0AFQ",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMDQyNDc5NiwianRpIjoiM2ZlYTFjY2UtYjdlNS00ZWI0LTljY2UtODYxYjI0YWMzNDgwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIzMDE5YzFhNC02Mzg4LTRiYmItYTEyMS01OTAxNzAyN2NhMTciLCJuYmYiOjE2MzA0MjQ3OTYsImV4cCI6MTYzMzAxNjc5Nn0.X6zrwIO-UBMvpBqQ96fhEW1W8sBwkjWuWLvLiPztNd8"
}
```

With this access token, you can create a new account for the user on the **POST** endpoint **/api/v1/accounts**:
```json
{
	"name": "Sample Account",
	"balance": 50.25
}
```

List the user accounts on the **GET** endpoint **/api/v1/accounts**:
```json
[
  {
    "id": "63c82a1b-e737-4c42-9a75-96424e9723d3",
    "name": "Sample Account",
    "income": "R$ 0,00",
    "expense": "R$ 0,00",
    "balance": "R$ 50,25"
  }
]
```

Verify the balance of a giver user account with the **GET** endpoint **/api/v1/accounts/{accountId}/balance**:
```json
{
  "balance": "R$ 50,25"
}
```

Create a new income/expense category with the **POST** endpoint **/api/v1/categories/**
```json
{
  "name": "Salário",
  "type": "E"
}
```

List all the user categories with the **GET** endpoint **/api/v1/categories/**:
```json
[
  {
    "id": "2f2189d5-fdca-4e8f-bb3c-c243a964b89c",
    "name": "Salário",
    "type": "Entrada"
  }
]
```

Create income transactions with the **POST** endpoint **/api/v1/transactions/{accountId}/income**:
```json
{
	"value": 1000.78,
	"category": "Salário"
}
```
Create expense transactions with the **POST** endpoint **/api/v1/transactions/{accountId}/expense**:
```json
{
	"value": 225.78,
	"category": "Mercado"
}
```
and finally list the transactions extract with the **GET** endpoint **/api/v1/transactions/{accountId}/extract**:
```json
[
  {
    "id": "8033508d-a530-44b9-a97f-db5c12623b87",
    "value": "R$ 1000,78",
    "created_at": "2021-08-27T13:32:37.633667",
    "category": {
      "id": "2f2189d5-fdca-4e8f-bb3c-c243a964b89c",
      "name": "Salário",
      "type": "Entrada"
    }
  },
  {
    "id": "7425bf49-bbbb-4445-b618-d193ebf21418",
    "value": "R$ 225,78",
    "created_at": "2021-08-27T13:32:53.639146",
    "category": {
      "id": "72a611ef-573a-4df5-8b47-49d210283ae9",
      "name": "Mercado",
      "type": "Saída"
    }
  }
]
```