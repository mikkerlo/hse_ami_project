from django.http import JsonResponse
from backend import models
from django.conf import settings
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from collections.abc import Iterable
import json

_STATUS_OK = 200
_STATUS_NOT_FOUND = 404
_STATUS_BAD_REQUEST = 400
_STATUS_UNAUTHORIZED = 401
_STATUS_FORBIDDEN = 403


def _get_user_permission(student_id, group_id):
    try:
        perm = models.GroupPermission.objects.get(
            student_id=student_id, group_id=group_id).permission_Level
    except models.GroupPermission.DoesNotExist:
        perm = models.GroupPermission.NOT_A_MEMBER
    return perm


def _check_perm(student_id, group_id, perm):
    return _get_user_permission(student_id, group_id) >= perm


def _can_modify_group(student_id, group_id):
    return _check_perm(student_id, group_id, models.GroupPermission.CREATOR)


def _can_modify_deadline(student_id, deadline):
    group_id = deadline.group_id.pk
    return _check_perm(student_id, group_id, models.GroupPermission.MODERATOR)


def _can_create_deadline(student_id, group_id):
    return _check_perm(student_id, group_id, models.GroupPermission.MODERATOR)


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
@api_method()
def upload_file(request):
    raw_file = request.FILES['file']

    name = request.POST.get('name', raw_file.name)

    file = models.File()
    file.name = name
    file.file = raw_file
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
    student_groups = student.group_set.prefetch_related('homework_set')
    homeworks = []
    for group in student_groups:
        homeworks.extend(group.homework_set.all())
    return _STATUS_OK, homeworks


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
        if not _can_modify_group(request.student, group):
            return _STATUS_FORBIDDEN, 'Only creator can edit the group'
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
    return _STATUS_OK, group.homework_set.all()


@require_GET
@api_method()
def group_students(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    return _STATUS_OK, group.students.all()


@require_POST
@api_method()
def group_new(request):
    data = json.loads(request.body)
    group = models.Group.from_json(data)
    group.student_creator = request.student
    group.save()
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
        permission = models.GroupPermission.objects.get(student=student, group=group)
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

    if not _can_modify_group(request.student.pk, group_id):
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


@require_GET
@api_method()
def deadlines_all(request):
    return _STATUS_OK, models.Homework.objects.all()


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
