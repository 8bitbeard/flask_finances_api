def test_application_instance(mocker):
    mock = mocker.patch('src.runner.create_app').return_value = mocker.Mock()
    mock.assert_called_once
