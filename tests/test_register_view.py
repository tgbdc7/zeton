import pytest
import re


def test_register_view_exists(client):
    # check if register endpoint exists
    response = client.get('/register')
    assert response.status_code == 200

