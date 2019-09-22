import pytest
from lxml import html


def test_not_logged_redirects_to_login_page(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'


CHILD_LOGIN = 'child_login'
CHILD_PASSWORD = 'child_password'
CHILD_FIRSTNAME = 'Bonifacy'


def test_logged_child_with_correct_credentials(client, auth):
    auth.login(CHILD_LOGIN, CHILD_PASSWORD)

    response = client.get("/")

    assert response.status_code == 200

    tree = html.fromstring(response.data)
    username_element = tree.xpath('//h3[@name="username"]')[0]
    username = username_element.text

    assert username == CHILD_FIRSTNAME


def test_logged_with_incorrect_credentials(client, auth):
    auth.login("non-existent-user", "wrong-password")

    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'
