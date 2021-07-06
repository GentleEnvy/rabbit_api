from rest_framework import serializers

from api.models import *

__all__ = [
    'FatteningRabbitDetailSerializer', 'BunnyDetailSerializer',
    'MotherRabbitDetailSerializer', 'FatherRabbitDetailSerializer'
]


def _create_detail_serializer(serializer_model):
    # noinspection PyMethodMayBeStatic
    class _Serializer(serializers.ModelSerializer):
        class __CageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Cage
                fields = ['farm_number', 'number', 'letter']

        class Meta:
            model = serializer_model
            fields = ['id', 'is_male', 'birthday', 'current_type', 'cage', 'status']
            depth = 1

        id = serializers.IntegerField(read_only=True)
        is_male = serializers.BooleanField(read_only=True)
        birthday = serializers.DateTimeField(read_only=True)
        current_type = serializers.CharField(read_only=True)
        cage = __CageSerializer(read_only=True)
        status = serializers.SerializerMethodField(read_only=True)

        def get_status(self, rabbit):
            return rabbit.cast.manager.status

    return _Serializer


FatteningRabbitDetailSerializer = _create_detail_serializer(FatteningRabbit)
BunnyDetailSerializer = _create_detail_serializer(Bunny)
MotherRabbitDetailSerializer = _create_detail_serializer(MotherRabbit)
FatherRabbitDetailSerializer = _create_detail_serializer(FatherRabbit)
