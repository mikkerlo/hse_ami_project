from django.http import JsonResponse
from backend import models
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from collections.abc import Iterable
import json

_STATUS_OK = 200
_STATUS_NOT_FOUND = 404
_STATUS_BAD_REQUEST = 400


def json_response(func):
    """Decorator, returning api specified json from view result.

    The view is expected to return a tuple of (status_code, result)"""
    def decorator(*args, **kwargs):
        try:
            status_code, result = func(*args, **kwargs)
        except Exception:
            # Unhandled exception caught. Returning 400 without any details.
            # TODO(solonkovda): log exception
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
            if isinstance(result, Iterable):
                json_result = []
                for el in result:
                    json_result.append(el.to_json())
            else:
                json_result = result.to_json()
            json_response = {
                'ok': True,
                'result': json_result,
            }
        return JsonResponse(json_response, status=status_code)
    return decorator


@require_GET
@json_response
def students_all(request):
    return _STATUS_OK, models.Student.objects.all()


@require_http_methods(['GET', 'PATCH'])
@json_response
def student_view(request, student_id):
    try:
        student = models.Student.objects.get(pk=student_id)
    except models.Student.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student not found'
    if request.method == 'GET':
        return _STATUS_OK, student
    else:
        data = json.loads(request.body)
        student.apply_json(data)
        student.save()
        return _STATUS_OK, student


@require_POST
@json_response
def student_new(request):
    data = json.loads(request.body)
    student = models.Student.from_json(data)
    student.save()
    return _STATUS_OK, student


@require_GET
@json_response
def student_deadlines(request, student_id):
    try:
        student = models.Student.objects.get(pk=student_id)
    except models.Student.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student not found'
    student_groups = student.group_set.prefetch_related('homework_set')
    homeworks = []
    for group in student_groups:
        homeworks.extend(group.homework_set.all())
    return _STATUS_OK, homeworks


@require_GET
@json_response
def groups_all(request):
    return _STATUS_OK, models.Group.objects.all()


@require_GET
@json_response
def student_groups(request, student_id):
    try:
        student = models.Student.objects.get(pk=student_id)
    except models.Student.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Student not found'
    student_groups = student.group_set.all()
    return _STATUS_OK, student_groups


@require_http_methods(['GET', 'PATCH'])
@json_response
def group_view(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    if request.method == 'GET':
        return _STATUS_OK, group
    else:
        data = json.loads(request.body)
        group.apply_json(data)
        group.save()
        return _STATUS_OK, group


@require_GET
@json_response
def group_deadlines(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    return _STATUS_OK, group.homework_set.all()


@require_GET
@json_response
def group_students(request, group_id):
    try:
        group = models.Group.objects.get(pk=group_id)
    except models.Group.DoesNotExist:
        return _STATUS_NOT_FOUND, 'Group not found'
    return _STATUS_OK, group.students.all()


@require_POST
@json_response
def group_new(request):
    data = json.loads(request.body)
    group = models.Group.from_json(data)
    group.save()
    return _STATUS_OK, group


@require_GET
@json_response
def deadlines_all(request):
    return _STATUS_OK, models.Homework.objects.all()


@require_http_methods(['GET', 'PATCH'])
@json_response
def deadline_view(request, deadline_id):
    try:
        deadline = models.Homework.objects.get(pk=deadline_id)
    except models.Homework.DoesNotExist:
        return 404, 'Deadline not found'
    if request.method == 'GET':
        return _STATUS_OK, deadline
    else:
        data = json.loads(request.body)
        deadline.apply_json(data)
        data.save()
        return _STATUS_OK, deadline


@require_POST
@json_response
def deadline_new(request):
    data = json.loads(request.body)
    deadline = models.Homework.from_json(data)
    deadline.group_id = models.Group.objects.get(pk=data['group_id'])
    deadline.save()
    return _STATUS_OK, deadline
