from rest_framework import status
from rest_framework.response import Response

from api.models import *
from api.views.base import BaseView
from api.views.model_views.utils import redirect_by_id
from api.views.model_views.base import BaseDetailView
from api.serializers import *

__all__ = [
    'RabbitDetailView', 'FatteningRabbitDetailView', 'BunnyDetailView',
    'MotherRabbitDetailView', 'FatherRabbitDetailView',
]


class RabbitDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        return redirect_by_id(
            Rabbit, request, kwargs.get('id'), current_type__in=(
                FatteningRabbit.CHAR_TYPE, Bunny.CHAR_TYPE, MotherRabbit.CHAR_TYPE,
                FatherRabbit.CHAR_TYPE
            )
        )


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
