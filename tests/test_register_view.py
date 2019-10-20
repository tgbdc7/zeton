import pytest
import re


def test_register_view_exists(client):
    # check if register endpoint exists
    response = client.get('/register')
    assert response.status_code == 200


def test_api_registration(client):
    # register with valid data
    response = client.post('/api/user', data={
        'username': 'testowy_1',
        'password': 'testowy_1',
        'email': 'testowy_1@example.com'
    })
    assert response.status_code == 302

    # register with username taken
    response = client.post('/api/user', data={
        'username': 'testowy_1',
        'password': 'testowy_1',
        'email': 'testowy_0@example.com'
    })
    assert response.status_code == 400

    # register with email taken
    response = client.post('/api/user', data={
        'username': 'testowy_1x',
        'password': 'testowy_1',
        'email': 'testowy_1@example.com'
    })
    assert response.status_code == 400

    # log in with the new account
    response = client.post('/login', data={
        'login': 'testowy_1',
        'password': 'testowy_1'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert re.search('Witaj testowy_1', response.get_data(as_text=True))


def test_register_with_missing_data(client):
    # register with username missing
    response = client.post('api/user', data={
        'username': None,
        'password': 'testowy_2'
    })
    assert response.status_code == 400

    # register with password missing
    response = client.post('/api/user', data={
        'username': 'testowy_3',
        'password': None
    })
    assert response.status_code == 400


