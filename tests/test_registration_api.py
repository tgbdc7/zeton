import re
from zeton.data_access import users


CAREGIVER_LOGIN = 'caregiver_login'
CAREGIVER_PASSWORD = 'caregiver_password'

DATASET_REGISTER = {
    'username': 'test_reg',
    'password': 'test_reg_pass',
    }

DATASET_ADD_CHILD = {
    'username': 'test_child',
    'password': 'test_child_pass',
    'role': 'child',
    'firstname': 'test_child_name'
    }

DATASET_ADD_CAREGIVER = {
    'username': 'test_caregiver',
    'password': 'test_pass',
    'role': 'caregiver',
    'firstname': 'test_caregiver_name'
    }


def test_api_registration(client):
    # register with valid data
    response = client.post('/api/user', data=DATASET_REGISTER)

    assert response.status_code == 302

    # register with username taken
    response = client.post('/api/user', data=DATASET_REGISTER)

    assert response.status_code == 400

    # log in with the new account
    response = client.post('/login', data={
        'login': 'test_reg',
        'password': 'test_reg_pass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert re.search('Witaj test_reg', response.get_data(as_text=True))


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


def test_api_add_person(app, auth):
    # login as caregiver

    client = app.test_client()
    client.post("/login", data={"login": CAREGIVER_LOGIN, "password": CAREGIVER_PASSWORD})

    # add new child
    response = client.post('api/user', data=DATASET_ADD_CHILD)
    assert response.status_code == 302

    with app.app_context():
        child = users.get_username_id_and_role_by_username('test_child')
        assert child['role'] == 'child'

    # add new caregiver
    response = client.post('api/user', data=DATASET_ADD_CAREGIVER)
    assert response.status_code == 302

    with app.app_context():
        child = users.get_username_id_and_role_by_username('test_caregiver')
        assert child['role'] == 'caregiver'

