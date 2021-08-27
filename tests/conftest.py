import pytest

from src import create_app
from src.database import db

from werkzeug.security import generate_password_hash

from src.models.users import User
from src.models.accounts import Account
from src.models.categories import Category
from src.models.transactions import Transaction


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

    print (user.password)

    db.session.add(user)
    db.session.commit()

    return user

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