import pytest
from flaskr.db import get_db

def test_index(auth, client):
    response = client.get('/')
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert b'test title' in response.data
    assert b'test\nbody' in response.data
    assert b'by test on 2018-01-01' in response.data

    auth.login
    response = client.get('/')
    assert b'Log out' in response.data
    assert b'href="/1/update"' in response.data

    
