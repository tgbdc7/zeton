import pytest
from lxml import html


def test_not_logged_redirects_to_login_page(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'


@pytest.mark.parametrize(('username', 'password', 'firstname'), (
        # ('caregiver_login', 'caregiver_password', 'Pafnucy'),  // TODO: fix for caregiver
        ('child_login', 'child_password', 'Bonifacy')
))
def test_logged_with_correct_credentials(client, auth, username, password, firstname):
    auth.login(username, password)

    response = client.get("/")

    assert response.status_code == 200

    tree = html.fromstring(response.data)
    username_element = tree.xpath('//div[@name="user_summary"]//h2[@name="username"]')[0]
    username = username_element.text

    assert username == firstname


def test_logged_with_incorrect_credentials(client, auth):
    auth.login("non-existent-user", "wrong-password")

    response = client.get("/")

    assert response.status_code == 302
    assert response.location == 'http://localhost/login'
