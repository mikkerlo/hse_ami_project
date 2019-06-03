from copy import copy

import pytest
from api.views import _STATUS_BAD_REQUEST
from api.views import _STATUS_UNAUTHORIZED
from api.views import _STATUS_OK

from backend.models import Group
from backend.models import GroupPermission
from backend.models import Student

from .fixtures import credentials
from .fixtures import users
from .fixtures import deadlines
from .fixtures import groups

from django.test import Client


@pytest.mark.django_db
def test_group_creation(client):
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        credentials[0],
        content_type='application/json'
    ).json()

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()

    assert r['ok']
    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    )

    assert r.status_code == 200
    group = r.json()['result']

    group_id = group['id']

    db_group = Group.objects.get(pk=group_id)

    groups[0]['id'] = group_id

    assert group == groups[0]


@pytest.mark.django_db
def test_group_access():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    group_id = r['result']['id']

    r = client.post(
        '/api/students/new/',
        credentials[1],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[1],
        content_type='application/json'
    ).json()

    assert r['ok']
    token = r['result']['token']

    r = client.get(
        f'/api/groups/{group_id}/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    )

    assert r
    assert r.status_code == 200


@pytest.mark.django_db
def test_group_update_ok():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    group_id = r['result']['id']

    new_group = copy(groups[0])
    new_group['full_name'] = 'asdf'
    new_group['id'] = group_id

    r = client.patch(
        f'/api/groups/{group_id}/',
        new_group,
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    assert r['result'] == new_group

    r = client.patch(
        f'/api/groups/{group_id}/',
        {},
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    assert r['result'] == new_group


@pytest.mark.django_db
def test_group_update_fail():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    group_id = r['result']['id']

    group_patch = {
        'is_hidden': '123'
    }
    r = client.patch(
        f'/api/groups/{group_id}/',
        group_patch,
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert not r['ok']


@pytest.mark.django_db
def test_group_students():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        users[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']
    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()
    assert r['ok']

    group_id = r['result']['id']

    r = client.get(
        f'/api/groups/{group_id}/students/',
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()

    assert r['ok']
    assert len(r['result']) == 1
    for field in ['name', 'telegram_account', 'username']:
        assert r['result'][0][field] == users[0][field]


@pytest.mark.django_db
def test_group_students():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        users[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']
    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()
    assert r['ok']

    deadlines[0].update({
        'group_id': r['result']['id']
    })

    r = client.post(
        f'/api/deadlines/new/',
        deadlines[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()
    assert r['ok']

    for field in ['content', 'created_at', 'group_id', 'header', 'valid_until']:
        assert r['result'][field] == deadlines[0][field]


@pytest.mark.django_db
def test_group_moderator():
    client = Client()
    assert client.post('/api/groups/new/').status_code == _STATUS_UNAUTHORIZED

    r = client.post(
        '/api/students/new/',
        users[0],
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        '/api/students/new/',
        users[1],
        content_type='application/json'
    ).json()
    assert r['ok']
    student_id = r['result']['id']

    r = client.post(
        '/api/auth/login/',
        credentials[0],
        content_type='application/json'
    ).json()
    assert r['ok']
    token = r['result']['token']

    r = client.post(
        f'/api/groups/new/',
        groups[0],
        content_type='application/json',
        HTTP_X_TOKEN=token
    ).json()
    assert r['ok']

    group_id = r['result']['id']

    r = client.post(
        f'/api/groups/{group_id}/add-moderator/',
        {'student_id': student_id},
        HTTP_X_TOKEN=token,
        content_type='application/json'
    ).json()
    assert not r['ok']

    permission = GroupPermission()
    permission.group = Group.objects.filter(pk=group_id)[0]
    permission.student = Student.objects.filter(pk=student_id)[0]
    permission.permission_level = GroupPermission.STUDENT
    permission.save()

    r = client.post(
        f'/api/groups/{group_id}/add-moderator/',
        {'student_id': student_id},
        HTTP_X_TOKEN=token,
        content_type='application/json'
    ).json()
    assert r['ok']

    r = client.post(
        f'/api/groups/{group_id}/remove-moderator/',
        {'student_id': student_id},
        HTTP_X_TOKEN=token,
        content_type='application/json'
    ).json()
    assert r['ok']

    assert GroupPermission.objects.filter(student_id=student_id)[
            0].permission_level == GroupPermission.STUDENT