import pytest

from src.services.categories_service import CategoriesService

from src.exceptions.categories_exception import CategoryNotFound, CategoryNameExists, CategoryInvalidType
from src.exceptions.users_exception import UserNotFound

def test_create_error_invalid_category_type():
    with pytest.raises(CategoryInvalidType):
        CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'invalid'})

def test_create_error_user_not_found(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None
    with pytest.raises(UserNotFound):
        CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'S'})

def test_create_error_category_name_already_exists(mock_get_sqlalchemy, mock_user_object):
    mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_user_object, True]
    with pytest.raises(CategoryNameExists):
        CategoriesService.create('user_id', {'name': 'CategoryName', 'type': 'S'})

def test_create_categories_service_method(mock_get_sqlalchemy, mock_user_object, mock_category_object, mocker):
    mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [mock_user_object, None]
    mocker.patch("src.services.users_service.db.session").return_value = mocker.Mock()
    category = CategoriesService.create(mock_user_object.id, {'name': mock_category_object.name, 'type': mock_category_object.type})
    assert category.id is not None
    assert category.user_id == mock_user_object.id
    assert category.name == mock_category_object.name
    assert category.type == mock_category_object.type

def test_index_categories_service_method(mock_get_sqlalchemy, mock_user_object, mock_category_object, mocker):
    mock_get_sqlalchemy.filter_by.return_value = [mock_category_object]
    categories = CategoriesService.index(mock_user_object.id)
    assert categories[0].id is not None
    assert categories[0].user_id is not None
    assert categories[0].name == mock_category_object.name
    assert categories[0].type == mock_category_object.type