import pytest
from flaskr.db import get_db

def test_index(auth, client):
    response = client.get('/')
    assert b"Login" in response.data
    assert b"Register" in response.data
    assert b'test title' in response.data
    assert b'test\nbody' in response.data
    assert b'by test on 2018-01-01' in response.data

    auth.login()
    response = client.get('/')
    assert b'Logout' in response.data
    assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # Current user can't modify other users posts:
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user can't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data = {'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

def test_update(auth, client, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': 'also updated'})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * from POST where id = 1').fetchone()
        assert post['title'] == 'updated'

@pytest.mark.parametrize( 'path', (
    '/1/update',
    '/create',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    # print(response.data)
    assert b'You need a title!' in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None