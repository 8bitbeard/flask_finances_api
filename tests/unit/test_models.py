def test_new_user(new_user):
    """
    Tests the creation of a new user
    """
    assert new_user.name == 'Unittest'
    assert new_user.email == 'unit_test@example.com'
    assert new_user.password == 'password'

def test_user_representation(new_user):
    """
    Tests the representation of the User entity
    """
    assert repr(new_user) == 'User>>> {}'.format(new_user.id)

def test_new_account_without_balance(new_account):
    """
    Tests the creation of a new account
    """
    assert new_account.name == 'Unit test'
    assert new_account.balance == 0
    assert new_account.income == 0
    assert new_account.expense == 0

def test_new_account_wit_balance(new_account_with_balance):
    """
    Tests the creation of a new account
    """
    assert new_account_with_balance.name == 'Unit test'
    assert new_account_with_balance.balance != 0
    assert new_account_with_balance.income == 0
    assert new_account_with_balance.expense == 0

def test_account_representation(new_account):
    """
    Tests the representation of the Account entity
    """
    assert repr(new_account) == 'Account>>> {}'.format(new_account.id)

def test_new_category(new_category):
    """
    Tests the creation of a new user
    """
    assert new_category.id != None
    assert new_category.name == 'UnitTest'
    assert new_category.type == 'E'
    assert new_category.user_id != None

def test_category_representation(new_category):
    """
    Tests the representation of the Category entity
    """
    assert repr(new_category) == 'Category>>> {}'.format(new_category.id)

def test_new_transaction(new_transaction):
    """
    Tests the creation of a new Transaction
    """
    assert new_transaction.id != None
    assert new_transaction.account_id != None
    assert new_transaction.value == 11.11
    assert new_transaction.category_id != None
    assert new_transaction.created_at != None

def test_transaction_representation(new_transaction):
    """
    Tests the representation of the Category entity
    """
    assert repr(new_transaction) == 'Transaction>>> {}'.format(new_transaction.id)