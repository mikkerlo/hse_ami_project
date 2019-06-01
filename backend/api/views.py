from django.http import JsonResponse
from backend import models
from backend import storage
from django.conf import settings
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from collections.abc import Iterable
import json
import time
import secrets

import logging
logger = logging.getLogger(__name__)

_STATUS_OK = 200
_STATUS_NOT_FOUND = 404
_STATUS_BAD_REQUEST = 400
_STATUS_UNAUTHORIZED = 401
_STATUS_FORBIDDEN = 403


def _get_user_permission(student_id, group_id):
    try:
        perm = models.GroupPermission.objects.get(
            student_id=student_id, group_id=group_id).permission_level
    except models.GroupPermission.DoesNotExist:
        perm = models.GroupPermission.NOT_A_MEMBER
    return perm


def _check_perm(student_id, group_id, perm):
    return _get_user_permission(student_id, group_id) >= perm


def _can_modify_group(student_id, group_id):
    return _check_perm(student_id, group_id, models.GroupPermission.CREATOR)


def _is_group_moderator(student_id, group_id):
    return _check_perm(student_id, group_id, models.GroupPermission.MODERATOR)


def _can_modify_deadline(student_id, deadline):
    group_id = deadline.group_id.pk
    return _check_perm(student_id, group_id, models.GroupPermission.MODERATOR)


def _can_create_deadline(student_id, group_id):
    return _check_perm(student_id, group_id, models.GroupPermission.MODERATOR)


class _StudentDeadlinesResult:
    """This class allows one to return permission along with content element."""
    def __init__(self, content_element, permission):
        self.content_element = content_element
        self.permission = permission

    def to_json(self):
        result = self.content_element.to_json()
        result['permission'] = self.permission
        return result


def _filter_deadlines(request, deadlines):
    if 'isDone' in request.GET:
        done_deadlines = set()
        for deadline in request.student.completed_homeworks.all():
            done_deadlines.add(deadline.pk)
        if request.GET['isDone'] == 1:
            deadlines = list(filter(
                lambda x: x.content_element.pk in done_deadlines,
                deadlines
            ))
        else:
            deadlines = list(filter(
                lambda x: x.content_element.pk not in done_deadlines,
                deadlines
            ))
    if 'isCurrent' in request.GET:
        current_time = time.time()
        if request.GET['isCurrent'] == 1:
            deadlines = list(filter(
                lambda x: x.content_element.valid_until >= current_time,
                deadlines
            ))
        else:
            deadlines = list(filter(
                lambda x: x.content_element.valid_until <= current_time,
                deadlines
            ))
    return deadlines


def validate_auth(func):
    """Decorator, validating authentication of the user."""
    def decorator(request, *args, **kwargs):
        user_token = request.META.get(settings.API_TOKEN_HEADER, None)
        if not user_token:
            return _STATUS_UNAUTHORIZED, 'No auth token found'
        try:
            token = models.AuthToken.objects.get(token=user_token)
        except models.AuthToken.DoesNotExist:
            return _STATUS_UNAUTHORIZED, 'Failed to resolve token'
        if not token.validate():
            return _STATUS_UNAUTHORIZED, 'Invalid auth token'
        request.student = token.student
        return func(request, *args, **kwargs)
    return decorator


def json_response(func):
    """Decorator, returning api specified json from view result.

    The view is expected to return a tuple of (status_code, result)"""
    def decorator(request, *args, **kwargs):
        try:
            status_code, result = func(request, *args, **kwargs)
        except Exception:
            logger.error('view returned exception', exc_info=True)
            # Unhandled exception caught. Returning 400 without any details.
            json_response = {
                'ok': False,
                'error': 'Internal error has occurred',
            }
            return JsonResponse(json_response, status=_STATUS_BAD_REQUEST)
        if status_code != _STATUS_OK:
            json_response = {
                'ok': False,
                'error': result,
            }
        else:
            if isinstance(result, dict):
                json_result = result
            elif isinstance(result, Iterable):
                json_result = []
                for el in result:
                    json_result.append(el.to_json())
            elif result is None:
                json_result = ''
            else:
                json_result = result.to_json()

            json_response = {
                'ok': True,
                'result': json_result,
            }
        return JsonResponse(json_response, status=status_code)
    return decorator


def api_method(require_auth=True):
    """Decorator, validating authentication of the user and returning json."""
    def wrapper(func):
        if not require_auth:
            return json_response(func)
        return json_response(validate_auth(func))
    return wrapper


@require_POST
@api_method(require_auth=False)
def auth_login(request):
    data = json.loads(request.body)

    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return _STATUS_UNAUTHORIZED, 'Login failed'
    token = models.AuthToken.create_token()
    token.student = user.student
    token.save()
    return _STATUS_OK, token


@require_POST
@api_method(require_auth=False)
def refresh_token(request):
    token_str = request.META.get(settings.API_TOKEN_HEADER, None)
    if token_str is None:
        return _STATUS_BAD_REQUEST, 'No token header found'
    try:
        token = models.AuthToken.objects.get(token=token_str)
    except models.AuthToken.DoesNotExist:
        return _STATUS_UNAUTHORIZED, 'Token not found or expired'
    if token.is_expired():
        return _STATUS_UNAUTHORIZED, 'Token not found or expired'
    new_token = models.AuthToken.create_token()
    new_token.student = token.student
    new_token.save()
    token.delete()
    return _STATUS_OK, new_token


@require_POST
@api_method(require_auth=False)
def change_password(request):
    data = json.loads(request.body)

    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new_password')

    user = authenticate(username=username, password=password)
    if user is None:
        return _STATUS_UNAUTHORIZED, 'Login failed'
    user.set_password(new_password)
    user.save()

    # Invalidating all user tokens
    models.AuthToken.objects.filter(student=user.student).delete()

    new_token = models.AuthToken.create_token()
    new_token.student = user.student
    new_token.save()

    return _STATUS_OK, new_token


@require_POST
@api_method(require_auth=False)
def upload_file(request):
    raw_file = request.FILES['file']
    name = request.POST.get('name', raw_file.name)

    bucket = storage.get_bucket()
    blob_name = secrets.token_urlsafe(10) + '/' + raw_file.name
    blob = bucket.blob(blob_name)
    blob.upload_from_file(raw_file)

    file = models.File()
    file.name = name
    file.blob_name = blob_name
    file.file_url = blob.public_url
    file.save()
    return _STATUS_OK, file


@require_POST
@api_method(require_auth=False)
def student_new(request):
    data = json.loads(request.body)

    username = data.get('username')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return _STATUS_BAD_REQUEST, 'Username already in use'

    student = models.Student.from_json(data)

    auth_user = User.objects.create_user(username, password=password)

    student.auth_user = auth_user
    student.save()

    return _STATUS_OK, student


@require_GET
@api_method()
def students_all(request):
    return _STATUS_OK, models.Student.objects.all()


@require_http_methods(['GET', 'PATCH'])
@api_method()
def student_view(request):
    student = request.student
    if request.method == 'GET':
        return _STATUS_OK, student
    else:
        data = json.loads(request.body)
        student.apply_json(data)
        student.save()
        return _STATUS_OK, student


@require_GET
@api_method()
def student_deadlines(request):
    student = request.student
    permissions = models.GroupPermission.objects.filter(
        student=student).select_related('group').\
        prefetch_related('group__homework_set')

    deadlines = []
    for permission in permissions:
        for homework in permission.group.homework_set.all():
            deadlines.append(
                _StudentDeadlinesResult(homework, permission.permission_level))

    return _STATUS_OK, _filter_deadlines(request, deadlines)


@require_GET
@api_method()
def groups_all(request):
    return _STATUS_OK, models.Group.objects.all()


@require_GET
@api_method()
def student_groups(request):
    student = request.student
    student_groups = student.group_set.all()
    return _STATUS_OK, student_groups


@require_http_methods(['GET', 'PATCH'])
@api_method()
def group_view(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    if request.method == 'GET':
        return _STATUS_OK, group
    else:
        if not _is_group_moderator(request.student, group):
            return _STATUS_FORBIDDEN, 'Only moderators can edit the group'
        data = json.loads(request.body)
        group.apply_json(data)
        group.save()
        return _STATUS_OK, group


@require_GET
@api_method()
def group_deadlines(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    permission = _get_user_permission(request.student.pk, group.pk)
    result = []
    for homework in group.homework_set.all():
        result.append(_StudentDeadlinesResult(homework, permission))
    return _STATUS_OK, _filter_deadlines(request, result)


@require_GET
@api_method()
def group_students(request, group_id):
    class GroupStudentsResponse:
        def __init__(self, student, permission):
            self.student = student
            self.permission = permission

        def to_json(self):
            result = self.student.to_json()
            result['permission'] = self.permission
            return result

    permissions = models.GroupPermission.objects.filter(group_id=group_id)

    result = []
    for permission in permissions:
        result.append(GroupStudentsResponse(permission.student,
                                            permission.permission_level))

    return _STATUS_OK, result


@require_POST
@api_method()
def group_new(request):
    data = json.loads(request.body)
    group = models.Group.from_json(data)
    group.save()

    permission = models.GroupPermission()
    permission.group = group
    permission.student = request.student
    permission.permission_level = models.GroupPermission.CREATOR
    permission.save()

    return _STATUS_OK, group


@require_POST
@api_method()
def group_add_moderator(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'

    if not _can_modify_group(request.student.pk, group_id):
        return _STATUS_FORBIDDEN, 'Only group creator can add moderators'

    data = json.loads(request.body)
    try:
        student = models.Student.objects.get(pk=data['student_id'])
    except models.Student.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student not found'

    try:
        permission = models.GroupPermission.objects.get(
            student=student, group=group)
    except models.GroupPermission.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student is not a member of the group'
    if permission.permission_level < models.GroupPermission.MODERATOR:
        permission.permission_level = models.GroupPermission.MODERATOR
        permission.save()
    return _STATUS_OK, None


@require_POST
@api_method()
def group_remove_moderator(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'

    if not _can_modify_group(request.student.pk, group_id):
        return _STATUS_FORBIDDEN, 'Only group creator can remove moderators'

    data = json.loads(request.body)
    try:
        student = models.Student.objects.get(pk=data['student_id'])
    except models.Student.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student not found'

    try:
        permission = models.GroupPermission.objects.get(student=student,
                                                        group=group)
        permission.permission_level = models.GroupPermission.STUDENT
        permission.save()
    except models.GroupPermission.DoesNotExist:
        pass
    return _STATUS_OK, None


@require_http_methods(['GET', 'POST', 'DELETE'])
@api_method()
def group_invite_token(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'

    if request.method != 'GET' and \
            not _can_modify_group(request.student.pk, group_id):
        return _STATUS_FORBIDDEN, 'Only group creator can edit invite tokens'

    if request.method == 'POST':
        group.generate_invite_token()
        group.save()
    elif request.method == 'DELETE':
        group.invite_token = None
        group.save()
    return _STATUS_OK, {'token': group.invite_token}


@require_POST
@api_method()
def use_invite_token(request):
    data = json.loads(request.body)
    token = data.get('token', '')
    try:
        group = models.Group.objects.get(invite_token=token)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Failed to resolve invite token'
    if not models.GroupPermission.objects.filter(
            student=request.student,
            group=group).exists():
        permission = models.GroupPermission()
        permission.group = group
        permission.student = request.student
        permission.permission_level = models.GroupPermission.STUDENT
        permission.save()
    return _STATUS_OK, group


@require_http_methods(['GET', 'PATCH'])
@api_method()
def deadline_view(request, deadline_id):
    try:
        deadline = models.Homework.objects.get(pk=deadline_id)
    except models.Homework.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Deadline not found'
    if request.method == 'GET':
        return _STATUS_OK, deadline
    else:
        if not _can_modify_deadline(request.student, deadline):
            return (
                _STATUS_FORBIDDEN,
                'Only group moderator or creator can edit this deadline'
            )
        data = json.loads(request.body)
        deadline.apply_json(data)
        deadline.save()
        deadline.apply_files(data)
        return _STATUS_OK, deadline


@require_http_methods(['POST', 'DELETE'])
@api_method()
def deadline_change_is_done(request, deadline_id):
    try:
        deadline = models.Homework.objects.get(pk=deadline_id)
    except models.Homework.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Deadline not found'
    if request.method == 'POST':
        request.student.completed_homeworks.add(deadline)
    else:
        request.student.completed_homeworks.remove(deadline)
    return _STATUS_OK, deadline


@require_POST
@api_method()
def deadline_new(request):
    data = json.loads(request.body)
    if not _can_create_deadline(request.student.pk, data['group_id']):
        return (_STATUS_FORBIDDEN,
                'Only moderator or creator can add deadlines to the group')
    deadline = models.Homework.from_json(data)
    deadline.group_id = models.Group.objects.get(pk=data['group_id'])
    deadline.save()
    deadline.apply_files(data)
    return _STATUS_OK, deadline
