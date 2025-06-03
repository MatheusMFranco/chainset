import pytest
from app import app, maps

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

def test_create_map_success(client):
    data = {
        'description': 'Mind map',
        'shape': 'circle',
        'border': 'solid',
        'text': 'Start here'
    }
    response = client.post('/chainset/maps', json=data)
    assert response.status_code == 201
    res_data = response.get_json()
    assert res_data['message'] == 'Map created!'
    assert res_data['map']['description'] == data['description']
    assert len(maps) > 0

@pytest.mark.parametrize('missing_field', ['description', 'shape', 'border', 'text'])
def test_create_map_missing_fields(client, missing_field):
    data = {
        'description': 'Mind map',
        'shape': 'circle',
        'border': 'solid',
        'text': 'Start here'
    }
    data.pop(missing_field)
    response = client.post('/chainset/maps', json=data)
    assert response.status_code == 400
    assert f'Field "{missing_field}" is required.' in response.get_json()['error']

def test_login_success(client):
    response = client.post('/chainset/login', json={'user': 'admin', 'password': 'admin'})
    assert response.status_code == 200
    token = response.get_json()['token']
    assert token is not None
