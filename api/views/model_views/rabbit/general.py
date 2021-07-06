from rest_framework.fields import HiddenField

from api.models import *
from api.serializers import *
from api.views.model_views.base import BaseGeneralView

__all__ = [
    'RabbitGeneralView', 'MotherRabbitGeneralView', 'FatherRabbitGeneralView'
]


class RabbitGeneralView(BaseGeneralView):
    list_serializer = RabbitGeneralSerializer
    queryset = Rabbit.objects.exclude(current_type=DeadRabbit.CHAR_TYPE).select_related(
        'bunny', 'bunny__cage',
        'fatteningrabbit', 'fatteningrabbit__cage',
        'motherrabbit', 'motherrabbit__cage',
        'fatherrabbit', 'fatherrabbit__cage'
    ).all()


class MotherRabbitGeneralView(BaseGeneralView):
    model = MotherRabbitCreateSerializer.Meta.model
    create_serializer = MotherRabbitCreateSerializer
    queryset = model.objects.all()


class FatherRabbitGeneralView(BaseGeneralView):
    model = FatherRabbitCreateSerializer.Meta.model
    create_serializer = FatherRabbitCreateSerializer
    queryset = model.objects.all()
