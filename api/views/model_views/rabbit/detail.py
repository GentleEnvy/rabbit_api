from urllib.parse import urlencode

from django.core.exceptions import FieldDoesNotExist, MultipleObjectsReturned
from django.shortcuts import redirect
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from api.models import *
from api.views.base import BaseView
from api.views.model_views.base import BaseDetailView
from api.views.model_views.rabbit._default_serializers import \
    create_default_retrieve_serializer

__all__ = [
    'RabbitDetailView', 'DeadRabbitDetailView', 'FatteningRabbitDetailView',
    'BunnyDetailView', 'MotherRabbitDetailView', 'FatherRabbitDetailView',
]


class RabbitDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            rabbit = Rabbit.objects.get(id=id)
        except (FieldDoesNotExist, MultipleObjectsReturned, APIException) as e:
            return exception_handler(e, {'request', request})
        if query_params := request.query_params:
            return redirect(f'{rabbit.get_absolute_url()}?{urlencode(query_params)}')
        return redirect(rabbit.get_absolute_url())


class DeadRabbitDetailView(BaseDetailView):
    model = DeadRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model)
    update_serializer = create_default_retrieve_serializer(model)


class FatteningRabbitDetailView(BaseDetailView):
    model = FatteningRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(model)


class BunnyDetailView(BaseDetailView):
    model = Bunny
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(model)


class MotherRabbitDetailView(BaseDetailView):
    model = MotherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(model)


class FatherRabbitDetailView(BaseDetailView):
    model = FatherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(model)
