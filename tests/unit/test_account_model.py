"""
Test file for account model
"""

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
