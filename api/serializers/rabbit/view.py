from api.serializers._base import BaseModelSerializer
from api.models import *

__all__ = [
    'RabbitSerializer', 'DeadRabbitSerializer', 'FatteningRabbitSerializer',
    'BunnySerializer', 'MotherRabbitSerializer', 'FatherRabbitSerializer'
]


class RabbitSerializer(BaseModelSerializer):
    class Meta:
        model = Rabbit
        fields = '__all__'


class DeadRabbitSerializer(BaseModelSerializer):
    class Meta:
        model = DeadRabbit
        fields = '__all__'


class FatteningRabbitSerializer(BaseModelSerializer):
    class Meta:
        model = FatteningRabbit
        fields = '__all__'


class BunnySerializer(BaseModelSerializer):
    class Meta:
        model = Bunny
        fields = '__all__'


class MotherRabbitSerializer(BaseModelSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'


class FatherRabbitSerializer(BaseModelSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'
