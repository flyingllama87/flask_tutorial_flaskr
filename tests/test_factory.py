from flaskr import create_app

def test_config():
    assert not create_app().test_config
    assert create_app({'TESTING': True}).TESTING
    
def test_hello():
    response = client.get('/hello')
    assert response.data == b'Hello world!!!'