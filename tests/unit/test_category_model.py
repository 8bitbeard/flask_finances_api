"""
Test file for category model
"""

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
