"""
Test file for transaction model
"""

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
