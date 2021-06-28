from urllib.parse import urlencode

from django.core.exceptions import FieldDoesNotExist, MultipleObjectsReturned
from django.shortcuts import redirect
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

__all__ = ['redirect_by_id']


def redirect_by_id(model, request, id):
    try:
        instance = model.objects.get(id=id)
    except (FieldDoesNotExist, MultipleObjectsReturned, APIException) as e:
        return exception_handler(e, {'request', request})
    if query_params := request.query_params:
        return redirect(f'{instance.cast.get_absolute_url()}?{urlencode(query_params)}')
    return redirect(instance.cast.get_absolute_url())
