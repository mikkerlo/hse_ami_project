import pytest

from api.views import _STATUS_OK, _STATUS_UNAUTHORIZED
from tests.fixtures import auth_user, students, deadlines


@pytest.mark.django_db
def test_deadlines_all(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get(
        '/api/deadlines/all/',
        HTTP_X_TOKEN=token
    )
    assert r.status_code == 200
    assert len(r.json()['result']) == len(deadlines)


@pytest.mark.django_db
def test_deadlines_view(client):
    deadline_id = 1
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.get(
        f'/api/deadlines/{deadline_id}/',
        HTTP_X_TOKEN=token
    )
    assert r.status_code == _STATUS_OK


@pytest.mark.django_db
def test_deadlines_new(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    data = {
        'created_at': 0,
        'header': 'test_1_deadline',
        'content': '',
        'valid_until': 1
    }

    r = client.post(
        '/api/deadlines/new',
        data,
        HTTP_X_TOKEN=token,
        content_type='application/json'
    )

    assert r.status_code == _STATUS_OK


