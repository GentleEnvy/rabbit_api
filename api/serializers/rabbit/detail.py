from rest_framework import serializers

from api.serializers.base import BaseReadOnlyRaiseSerializer
from api.models import *

__all__ = [
    'FatteningRabbitDetailSerializer', 'BunnyDetailSerializer',
    'MotherRabbitDetailSerializer', 'FatherRabbitDetailSerializer'
]


def _create_detail_serializer(serializer_model):
    # noinspection PyMethodMayBeStatic
    class _Serializer(BaseReadOnlyRaiseSerializer):
        class __CageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Cage
                fields = ['farm_number', 'number', 'letter']

        class Meta:
            model = serializer_model
            read_only_fields = [
                'id', 'is_male', 'birthday', 'breed', 'current_type', 'cage', 'status'
            ]
            fields = read_only_fields + ['weight']
            depth = 1

        cage = __CageSerializer(read_only=True)
        status = serializers.SerializerMethodField()
        breed = serializers.SerializerMethodField()

        def get_status(self, rabbit):
            return rabbit.cast.manager.status

        def get_breed(self, rabbit):
            return rabbit.breed.title

    return _Serializer


FatteningRabbitDetailSerializer = _create_detail_serializer(FatteningRabbit)
BunnyDetailSerializer = _create_detail_serializer(Bunny)
MotherRabbitDetailSerializer = _create_detail_serializer(MotherRabbit)
FatherRabbitDetailSerializer = _create_detail_serializer(FatherRabbit)
