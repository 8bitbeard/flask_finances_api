# type: ignore

"""
Test file for categories_service.py
"""


import pytest

from src.services.categories_service import CategoriesService

from src.exceptions.categories_exception import CategoryNameExists, CategoryInvalidType
from src.exceptions.users_exception import UserNotFound


class TestCreate:
    """
    Create method test grouping class
    """

    def test_create_error_invalid_category_type(self):
        """
        Test if create method raises an CategoryInvalidType when passing a invalid type on type parameter
        """
        with pytest.raises(CategoryInvalidType):
            CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'invalid'})

    def test_create_error_user_not_found(self, mock_get_sqlalchemy):
        """
        Test if create method raises an UserNotFound when the user_id do not correspond to any user
        """
        mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
        with pytest.raises(UserNotFound):
            CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'S'})

    def test_create_error_category_name_already_exists(self, mock_get_sqlalchemy, mock_user_object):
        """
        Test if create method raises an CategoryNameExists when informing a category name already taken
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_user_object, True]
        with pytest.raises(CategoryNameExists):
            CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'S'})

    def test_create_categories_service_method( self, mock_get_sqlalchemy, mock_user_object, mock_s_category_object, mocker):
        """
        Test if create method creates a category with success
        """
        mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_user_object, None]
        mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
        category = CategoriesService.create(mock_user_object.id, {'name': mock_s_category_object.name, 'type': mock_s_category_object.type.name})
        assert category.id is not None
        assert category.user_id == mock_user_object.id
        assert category.name == mock_s_category_object.name
        assert category.type == mock_s_category_object.type.name


class TestIndex:
    """
    Index method test grouping class
    """

    def test_index_categories_service_method(self, mock_get_sqlalchemy, mock_user_object, mock_s_category_object):
        """
        Test if index method returns a list of existing categories
        """
        mock_get_sqlalchemy.filter_by.return_value = [mock_s_category_object]
        categories = CategoriesService.index(mock_user_object.id)
        assert categories[0].id == mock_s_category_object.id
        assert categories[0].user_id == mock_s_category_object.user_id
        assert categories[0].name == mock_s_category_object.name
        assert categories[0].type == mock_s_category_object.type

