"""
Test file for user model
"""

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
