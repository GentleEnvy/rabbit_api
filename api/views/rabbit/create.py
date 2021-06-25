from rest_framework.generics import CreateAPIView

from api.serializers.rabbit.create import *

__all__ = [
    'FatteningRabbitCreateView', 'BunnyCreateView', 'MotherRabbitCreateView',
    'FatherRabbitCreateView'
]


class FatteningRabbitCreateView(CreateAPIView):
    serializer_class = FatteningRabbitCreateSerializer


class BunnyCreateView(CreateAPIView):
    serializer_class = BunnyCreateSerializer


class MotherRabbitCreateView(CreateAPIView):
    serializer_class = MotherRabbitCreateSerializer


class FatherRabbitCreateView(CreateAPIView):
    serializer_class = FatherRabbitCreateSerializer
