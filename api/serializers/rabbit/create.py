from api.serializers._base import BaseModelSerializer
from api.models import *

__all__ = [
    'FatteningRabbitCreateSerializer', 'BunnyCreateSerializer',
    'MotherRabbitCreateSerializer', 'FatherRabbitCreateSerializer'
]


class FatteningRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = FatteningRabbit
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data | {
            'current_type': FatteningRabbit.TYPE_FATTENING
        })


class BunnyCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Bunny
        fields = '__all__'


class MotherRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'


class FatherRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'
