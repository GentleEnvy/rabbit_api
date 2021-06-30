from rest_framework.fields import *

from api.models import *
from api.views.base import BaseView
from api.views.model_views._utils import redirect_by_id
from api.views.model_views.base import BaseDetailView
from api.views.model_views.rabbit._default_serializers import *

__all__ = [
    'RabbitDetailView', 'DeadRabbitDetailView', 'FatteningRabbitDetailView',
    'BunnyDetailView', 'MotherRabbitDetailView', 'FatherRabbitDetailView',
]


class RabbitDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        return redirect_by_id(Rabbit, request, kwargs.get('id'))


class DeadRabbitDetailView(BaseDetailView):
    model = DeadRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model)
    update_serializer = create_default_retrieve_serializer(
        model, is_male_field=BooleanField(read_only=True)
    )
    queryset = model.objects.all()


class FatteningRabbitDetailView(BaseDetailView):
    model = FatteningRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(
        model, is_male_field=BooleanField(read_only=True)
    )
    queryset = model.objects.all()


class BunnyDetailView(BaseDetailView):
    model = Bunny
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(model)
    queryset = model.objects.all()


class MotherRabbitDetailView(BaseDetailView):
    model = MotherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(
        model, is_male_field=BooleanField(read_only=True)
    )
    queryset = model.objects.all()


class FatherRabbitDetailView(BaseDetailView):
    model = FatherRabbit
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model, 1)
    update_serializer = create_default_retrieve_serializer(
        model, is_male_field=BooleanField(read_only=True)
    )
    queryset = model.objects.all()
