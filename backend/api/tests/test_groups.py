import pytest

from api.views import _STATUS_OK, _STATUS_UNAUTHORIZED
from tests.fixtures import auth_user, student, students, groups, deadlines


@pytest.mark.django_db
def test_groups(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get('/api/groups/all/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    assert len(r.json()['result']) == len(groups)


@pytest.mark.django_db
def test_group_view(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.get('/api/groups/all/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    group_id = r.json()['result'][0]['id']

    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.get(f'/api/groups/{group_id}/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    data = r.json()['result']
    for field in ['full_name', 'short_name', 'is_hidden']:
        assert data[field] == groups[0][field]


@pytest.mark.django_db
def test_group_deadlines(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get(f'/api/groups/1/deadlines/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    data = r.json()['result']
    assert len(data) == len(deadlines)

    for field in ['created_at', 'header', 'valid_until']:
        assert data[0][field] == deadlines[0][field]


@pytest.mark.django_db
def test_group_students(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.get(f'/api/groups/1/students/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    data = r.json()['result']

    assert data[0]['name']['first_name'] == students[0]['first_name']
    assert data[0]['name']['last_name'] == students[0]['last_name']


@pytest.mark.django_db
def test_group_creation(client):
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    data = {
        'full_name': 'test_creation',
        'short_name': 'creation',
        'is_hidden': False,
        'description': ''
    }

    r = client.post(
        f'/api/groups/new/',
        data,
        HTTP_X_TOKEN=token,
        content_type='application/json'
    )
    assert r.status_code == 200
    group_id = r.json()['result']['id']

    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    data.update({'id': group_id})
    r = client.get(
        f'/api/groups/{group_id}/',
        HTTP_X_TOKEN=token
    )
    assert r.status_code == _STATUS_OK
    assert r.json()['result'] == data

