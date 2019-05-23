import pytest
from backend.models import Student
from api.views import _STATUS_UNAUTHORIZED
from django.contrib.auth.models import User

from tests.fixtures import auth_user, student, students


@pytest.mark.django_db
def test_login_ok(client):
    r = client.post(
        '/api/auth/login/',
        {'username': students[0]['username'],
         'password': students[0]['password']}
    )
    assert r.status_code == 200


@pytest.mark.django_db
def test_login_fail(client):
    r = client.post(
        '/api/auth/login/',
        {'username': 'n', 'password': '1'},
    )
    assert r.status_code == _STATUS_UNAUTHORIZED
