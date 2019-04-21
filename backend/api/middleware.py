from django.http import JsonResponse
from json import JSONDecodeError
from django.db.utils import IntegrityError
from .exceptions import AMIBaseException


class ExceptionHandlerMiddleware():
    """
    Middleware for handling exceptions. Makes it more clear to code.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, *args, **kwargs):
        return self.get_response(*args, **kwargs)

    def process_exception(self, request, exception):
        if isinstance(exception, AMIBaseException):
            result = {
                'ok': False,
                'error': exception.error
            }
            return JsonResponse(result, status=exception.status_code)
        if isinstance(exception, JSONDecodeError):
            result = {
                'ok': False,
                'error': 'Could not parse JSON object, check API'
            }
            return JsonResponse(result, status=400)
        if isinstance(exception, IntegrityError):
            result = {
                'ok': False,
                'error': f'Internal integrity error occured: {exception}'
            }
            return JsonResponse(result, status=400)
        else:
            return None
