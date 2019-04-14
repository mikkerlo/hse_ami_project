from django.http import JsonResponse
from backend import models
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections.abc import Iterable
import json


def json_response(func):
    """Decorator, returning api specified json from view result.

    The view is expected to return a tuple of (status_code, result)"""
    def decorator(*args, **kwargs):
        try:
            status_code, result = func(*args, **kwargs)
        except models.Student.DoesNotExist as e:
            # Unhandled exception caught. Returning 400 without any details.
            print(str(e))
            json_response = {
                'ok': False,
                'error': 'Internal error has occurred',
            }
            return JsonResponse(json_response, status=400)
        json_response = dict()
        if status_code != 200:
            json_response['ok'] = False
            json_response['error'] = result
        else:
            json_response['ok'] = True
            if isinstance(result, Iterable):
                json_response['response'] = []
                for el in result:
                    json_response['response'].append(el.to_json())
            else:
                json_response['response'] = result.to_json()
        return JsonResponse(json_response, status=status_code)
    return decorator


@require_GET
@csrf_exempt
@json_response
def students_all(request):
    return 200, models.Student.objects.all().order_by('pk')


@require_http_methods(['GET', 'PATCH'])
@csrf_exempt
@json_response
def student_view(request, id):
    if request.method == 'GET':
        try:
            student = models.Student.objects.get(pk=id)
            return 200, student
        except models.Student.DoesNotExist:
            return 404, 'Student not found'
    else:
        data = json.loads(request.body)
        try:
            student = models.Student.objects.get(pk=id)
        except models.Student.DoesNotExist:
            return 404, 'Student not found'
        student.apply_json(data)
        student.save()
        return 200, student
