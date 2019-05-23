import pytest

from api.views import _STATUS_OK
from tests.fixtures import auth_user, student, students, deadlines


@pytest.mark.django_db
def test_students_all_ok(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == _STATUS_OK

    token = r.json()['result']['token']

    r = client.get('/api/students/all/', HTTP_X_TOKEN=token)

    assert r.status_code == 200
    assert len(r.json()['result']) == len(students)


@pytest.mark.django_db
def test_student_view_get_ok(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get('/api/students/student/', HTTP_X_TOKEN=token)
    print(token)
    assert r.status_code == 200


@pytest.mark.django_db
def test_student_view_patch_ok(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.patch(
        '/api/students/student/',
        {"name": {"first_name": "1"}},
        content_type='application/json',
        HTTP_X_TOKEN=token
    )

    assert r.status_code == 200

    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']
    r = client.get(
        '/api/students/student/', HTTP_X_TOKEN=token
    )
    assert r.status_code == _STATUS_OK
    assert r.json()['result']['name']['first_name'] == '1'


@pytest.mark.django_db
def test_student_new_ok(client):
    registration_data = {
        'username': 'user2',
        'password': 'pass',
    }

    student_data = {
        'name': {
            'first_name': 'user2_first_name',
            'last_name': 'user2_last_name'
        }
    }
    student_data.update(registration_data)

    r = client.post('/api/students/new/', student_data,
                    content_type='application/json')

    assert r.status_code == 200

    r = client.post('/api/auth/login/', registration_data)
    print(r.json())
    assert r.status_code == 200


@pytest.mark.django_db
def test_student_deadlines(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get('/api/students/deadlines/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    assert len(r.json()['result']) == len(deadlines)


@pytest.mark.django_db
def test_student_groups(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )

    assert r.status_code == _STATUS_OK
    token = r.json()['result']['token']

    r = client.get('/api/students/groups/', HTTP_X_TOKEN=token)
    assert r.status_code == 200
    assert len(r.json()['result']) == 1
