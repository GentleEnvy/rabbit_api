from rest_framework.fields import *

from api.models import *
from api.views.base import BaseView
from api.views.model_views._utils import redirect_by_id
from api.views.model_views.base import BaseDetailView
from api.serializers import *

__all__ = [
    'RabbitDetailView', 'FatteningRabbitDetailView', 'BunnyDetailView',
    'MotherRabbitDetailView', 'FatherRabbitDetailView',
]


class RabbitDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        return redirect_by_id(Rabbit, request, kwargs.get('id'), current_type__in=[
            FatteningRabbit.CHAR_TYPE, Bunny.CHAR_TYPE, MotherRabbit.CHAR_TYPE,
            FatherRabbit.CHAR_TYPE
        ])


class FatteningRabbitDetailView(BaseDetailView):
    model = FatteningRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = FatteningRabbitDetailSerializer
    update_serializer = FatteningRabbitDetailSerializer
    queryset = model.objects.all()


class BunnyDetailView(BaseDetailView):
    model = Bunny
    lookup_url_kwarg = 'id'
    retrieve_serializer = BunnyDetailSerializer
    update_serializer = BunnyDetailSerializer
    queryset = model.objects.all()


class MotherRabbitDetailView(BaseDetailView):
    model = MotherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = MotherRabbitDetailSerializer
    update_serializer = MotherRabbitDetailSerializer
    queryset = model.objects.all()


class FatherRabbitDetailView(BaseDetailView):
    model = FatherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = FatherRabbitDetailSerializer
    update_serializer = FatherRabbitDetailSerializer
    queryset = model.objects.all()
