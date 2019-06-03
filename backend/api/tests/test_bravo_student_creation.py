import pytest
from .fixtures import users, credentials, illegal_users
import json
from pprint import pprint

from backend.models import Student


@pytest.mark.django_db
def test_student_new_ok(client):
    r = client.post(
        '/api/students/new/',
        users[0],
        content_type='application/json'
    )

    assert r.status_code == 200
    data = r.json()['result']

    for key in ['name', 'telegram_account', 'username']:
        assert users[0][key] == data[key]

    db_student_object = Student.objects.filter(pk=data['id'])[0]
    for key in ['name', 'telegram_account', 'username']:
        assert users[0][key] == db_student_object.to_json()[key]


@pytest.mark.skip() # Remove after backend refactoring
@pytest.mark.parametrize('user', illegal_users)
@pytest.mark.django_db
def test_student_new_fail(client, user):
    r = client.post(
        '/api/students/new/',
        user,
        content_type='application/json'
    )

    print(user)
    assert r.status_code == 400

