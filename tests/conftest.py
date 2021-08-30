import pytest
import decimal
from uuid import uuid4
from datetime import datetime

from src import create_app
from src.database import db

from werkzeug.security import generate_password_hash

from src.models.users import User
from src.models.accounts import Account
from src.models.categories import Category, CategoryType
from src.models.transactions import Transaction

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture
def app():
    """ Instance of Main flask app """
    app = create_app(config_name='testing')
    return app

@pytest.fixture
def test_client():
    app = create_app(config_name='testing')
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture
def init_database():

    db.create_all()

    yield db

    db.session.close()

    db.drop_all()

@pytest.fixture
def insert_user_db():
    user = User(name='Mock User', email='mock_user@example.com', password=generate_password_hash('password'))

    db.session.add(user)
    db.session.commit()

    return user

@pytest.fixture
def insert_account_db(insert_user_db):
    account = Account(name='Unit test', user_id=insert_user_db.id, balance=10.25)

    db.session.add(account)
    db.session.commit()

    return account

@pytest.fixture
def insert_income_category_db(insert_user_db):
    category = Category(name='UnitTest', type='E', user_id=insert_user_db.id)

    db.session.add(category)
    db.session.commit()

    return category

@pytest.fixture
def insert_expense_category_db(insert_user_db):
    category = Category(name='UnitTest', type='S', user_id=insert_user_db.id)

    db.session.add(category)
    db.session.commit()

    return category

@pytest.fixture
def insert_income_transaction_db(insert_user_db, insert_account_db, insert_income_category_db):
    transaction = Transaction(account_id = insert_account_db.id, value=10.25, category_id=insert_income_category_db.id)

    db.session.add(transaction)
    db.session.commit()

    return transaction

@pytest.fixture
def insert_expense_transaction_db(insert_user_db, insert_account_db, insert_expense_category_db):
    transaction = Transaction(account_id = insert_account_db.id, value=10.25, category_id=insert_expense_category_db.id)

    db.session.add(transaction)
    db.session.commit()

    return transaction

@pytest.fixture
def new_user():
    user = User(name='Unittest', email='unit_test@example.com', password='password')
    return user

@pytest.fixture
def new_account(new_user):
    account = Account(name='Unit test', user_id=new_user.id)
    return account

@pytest.fixture
def new_account_with_balance(new_user):
    account = Account(name='Unit test', user_id=new_user.id, balance=10.25)
    return account

@pytest.fixture
def new_category(new_user):
    category = Category(name='UnitTest', type='E', user_id=new_user.id)
    return category

@pytest.fixture
def new_transaction(new_account):
    category = Category(name='UnitTest', type='E', user_id=new_account.user_id)
    transaction = Transaction(account_id=new_account.id, value=11.11, category_id=category.id)
    return transaction

@pytest.fixture
def mock_user_object():
    user = User(
        id=uuid4(),
        name="Mock User",
        email="mock_user@example.com",
        password="password",
        created_at = datetime.now(),
        updated_at = None
    )
    return user

@pytest.fixture
def mock_account_object():
    account = Account(
        id = uuid4(),
        name = 'Mock Account',
        user_id = uuid4(),
        balance = decimal.Decimal(10.25),
        income = decimal.Decimal(0),
        expense = decimal.Decimal(0)
    )
    return account

@pytest.fixture
def mock_e_category_object():
    category = Category(
        id = uuid4(),
        name = 'Income Category',
        type = CategoryType.E,
        user_id = uuid4()
    )
    return category

@pytest.fixture
def mock_s_category_object():
    category = Category(
        id = uuid4(),
        name = 'Expense Category',
        type = CategoryType.S,
        user_id = uuid4()
    )
    return category

@pytest.fixture
def mock_transaction_object():
    transaction = Transaction(
        id = uuid4(),
        account_id = uuid4(),
        value = decimal.Decimal(1),
        category_id = uuid4(),
        created_at = datetime.now()
    )
    return transaction

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
    return mock
