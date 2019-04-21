from django.http import JsonResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from api import AMIBaseException

print()
from api.data_manager import deadlines
import json

from pprint import pprint

_STATUS_OK = 200
_STATUS_NOT_FOUND = 404
_STATUS_BAD_REQUEST = 400


@csrf_exempt
@require_http_methods(['GET'])
def all(request: HttpRequest):
    result = {
        'ok': True,
        'result': deadlines.all(request)
    }
    return JsonResponse(result, status=200)


@csrf_exempt
@require_http_methods(['GET', 'PATCH'])
def by_id(request: HttpRequest, id: int):
    if request.method == 'GET':
        result = {
            'ok': True,
            'result': deadlines.get_by_id(request, id)
        }
        return JsonResponse(result, status=200)
    elif request.method == 'PATCH':
        result = {
            'ok': True,
            'result': deadlines.update_by_id(request, id)
        }
        return JsonResponse(result, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def new(request: HttpRequest):
    result = {
        'ok': True,
        'result': deadlines.new(request)
    }
    return JsonResponse(result, status=200)
