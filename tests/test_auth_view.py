from lxml import html


def test_not_logged_redirects_to_login_page(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'


def test_logged_with_correct_credentials(client, auth):
    auth.login("dziecko1", "dziecko1")

    response = client.get("/")

    assert response.status_code == 200

    tree = html.fromstring(response.data)
    username_element = tree.xpath('//div[@name="user_summary"]//h2[@name="username"]')[0]
    username = username_element.text

    assert username == 'Bazyli'


def test_logged_with_incorrect_credentials(client, auth):
    auth.login("non-existent-user", "wrong-password")

    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'
