from django.db.models import QuerySet
from django.http import HttpRequest

from api.exceptions import DeadlineDoesNotExists, GroupDoesNotExists
from backend.models import Homework, Group
import json


def all(request):
    query_result: QuerySet = Homework.objects.all().order_by('pk')

    result = list()
    for element in query_result:
        result.append(element.to_json())

    return result


def get_by_id(request: HttpRequest, id: int):
    try:
        query_result = Homework.objects.get(pk=id)
    except Homework.DoesNotExist as exception:
        # Thank you Django for this perfect behaviour. You can not import model class exception
        # in middleware. THANKS
        raise DeadlineDoesNotExists(id)

    return query_result.to_json()


def update_by_id(request: HttpRequest, id: int):
    try:
        object = Homework.objects.get(pk=id)
        object.apply_json(json.loads(request.body))
        object.save()
        return True
    except Homework.DoesNotExist as exception:
        raise DeadlineDoesNotExists(id)
    # TODO(nikitaorlov): Check what to do if we could not save instance


def new(request: HttpRequest):
    data = json.loads(request.body)
    object = Homework.from_json(data)
    try:
        object.group_id = Group.objects.get(pk=data['group_id'])
    except Group.DoesNotExist:
        raise GroupDoesNotExists(data['group_id'])
    object.save()
    return object.to_json()
