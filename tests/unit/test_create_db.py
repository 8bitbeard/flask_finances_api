def test_create_db(mocker):
    mock = mocker.patch('src.database.create_db.db').return_value = mocker.Mock()
    mocker.patch('src.database.create_db.create_app').return_value = mocker.Mock()
    mocker.patch('src.database.create_db.os.environ').return_value = mocker.Mock()
    mock.assert_called_once

