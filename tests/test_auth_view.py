def test_not_logged_redirects_to_login_page(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'


def test_logged_with_correct_credentials(client, auth):
    auth.login("dziecko1", "dziecko1")

    response = client.get("/")

    assert response.status_code == 200
    assert b'Bazyli' in response.data  # TODO: very naive test, needs to be changed


def test_logged_with_incorrect_credentials(client, auth):
    auth.login("non-existant-user", "wrong-password")

    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'
