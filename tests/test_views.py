import pytest
import re


def test_register_view_exists(client):
    # check if register endpoint exists
    response = client.get('/register')
    assert response.status_code == 200


def test_add_person_view_exists(client):
    # check if register endpoint exists
    response = client.get('/add-person')
    assert response.status_code == 200

