def test_app_is_created(app):
    assert app.name == 'src'

def test_request_returns_404(test_client):
    assert test_client.get("/url_que_nao_existe").status_code == 404

def test_request_returns_500(test_client):
    assert test_client.get("/error_500").status_code == 500