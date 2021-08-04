from urllib.parse import urlencode

from django.http import Http404
from django.shortcuts import redirect

from api.models import *
from api.views.base import BaseView
from api.views.model_views.base import BaseDetailView
from api.serializers import *

__all__ = [
    'RabbitDetailView', 'FatteningRabbitDetailView', 'BunnyDetailView',
    'MotherRabbitDetailView', 'FatherRabbitDetailView',
]


class RabbitDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, id):
        try:
            base_rabbit = Rabbit.objects.get(
                id=id, current_type__in=(
                    FatteningRabbit.CHAR_TYPE, Bunny.CHAR_TYPE, MotherRabbit.CHAR_TYPE,
                    FatherRabbit.CHAR_TYPE
                )
            )
        except Rabbit.DoesNotExist:
            raise Http404('Rabbit with this id was not found')
        if query_params := request.query_params:
            return redirect(
                f'{base_rabbit.cast.get_absolute_url()}?{urlencode(query_params)}'
            )
        return redirect(base_rabbit.cast.get_absolute_url())


class _BaseRabbitDetailView(BaseDetailView):
    lookup_url_kwarg = 'id'


class FatteningRabbitDetailView(_BaseRabbitDetailView):
    model = FatteningRabbit
    queryset = FatteningRabbit.objects.all()
    retrieve_serializer = FatteningRabbitDetailSerializer
    update_serializer = FatteningRabbitDetailSerializer


class BunnyDetailView(_BaseRabbitDetailView):
    model = Bunny
    queryset = Bunny.objects.all()
    retrieve_serializer = BunnyDetailSerializer
    update_serializer = BunnyDetailSerializer


class MotherRabbitDetailView(_BaseRabbitDetailView):
    model = MotherRabbit
    queryset = MotherRabbit.objects.prefetch_related('rabbit_set').all()
    retrieve_serializer = MotherRabbitDetailSerializer
    update_serializer = MotherRabbitDetailSerializer


class FatherRabbitDetailView(_BaseRabbitDetailView):
    model = FatherRabbit
    queryset = FatherRabbit.objects.all()
    retrieve_serializer = FatherRabbitDetailSerializer
    update_serializer = FatherRabbitDetailSerializer
