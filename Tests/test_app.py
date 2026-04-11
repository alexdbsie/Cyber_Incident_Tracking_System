import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': '1234'
    })
    assert response.status_code == 200

def test_login(client):
    client.post('/register', data={
        'username': 'testuser2',
        'password': '1234'
    })

    response = client.post('/login', data={
        'username': 'testuser2',
        'password': '1234'
    })

    assert response.status_code == 302