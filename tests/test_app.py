import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_warning_route_returns_nothing(client):
    response = client.get('/warning')
    assert response.status_code == 200
    assert b'No items to show' in response.data

def test_warning_route_returns_list(client):
    items = ['apple', 'banana', 'orange']
    response = client.get('/warning?' + '&'.join(f'item={i}' for i in items))
    html = response.data.decode('utf-8')
    assert response.status_code == 200
    assert f'This set includes { len(items) } items:' in html
    for item in items:
        assert item.upper() in html

def test_welcome_no_token(client):
    response = client.get('/chainset/welcome')
    assert response.status_code == 401
    assert 'Token is away!' in response.get_json()['message']