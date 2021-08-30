def test_create_db(mocker):
    mock = mocker.patch('src.database.create_db.db').return_value = mocker.Mock()
    mock.assert_called_once

