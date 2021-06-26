from urllib.parse import urlencode

from django.shortcuts import redirect
from django.core.exceptions import FieldDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView, exception_handler
from rest_framework.exceptions import APIException

from api.models import *

__all__ = [
    'RabbitView'
]


# noinspection PyMethodMayBeStatic
class RabbitView(APIView):
    def get(self, request, id):
        try:
            rabbit = Rabbit.objects.get(id=id)
        except (FieldDoesNotExist, MultipleObjectsReturned, APIException) as e:
            return exception_handler(e, {'request', request})
        if query_params := request.query_params:
            return redirect(f'{rabbit.get_absolute_url()}?{urlencode(query_params)}')
        return redirect(rabbit.get_absolute_url())
