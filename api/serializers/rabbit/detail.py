
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            read_only_fields = [
                'id', 'is_male', 'birthday', 'current_type', 'cage', 'status'
            ]
            fields = read_only_fields + ['weight']
            depth = 1

        cage = __CageSerializer(read_only=True)
        status = serializers.SerializerMethodField(read_only=True)

        def to_internal_value(self, data):
            print(data)
            for read_only_field in self.Meta.read_only_fields:
                if read_only_field in data:
                    raise ValidationError({
                        read_only_field: f'{read_only_field} is read only'
                    })
            return super().to_internal_value(data)

        def get_status(self, rabbit):
            return rabbit.cast.manager.status

    return _Serializer


FatteningRabbitDetailSerializer = _create_detail_serializer(FatteningRabbit)
BunnyDetailSerializer = _create_detail_serializer(Bunny)
MotherRabbitDetailSerializer = _create_detail_serializer(MotherRabbit)
FatherRabbitDetailSerializer = _create_detail_serializer(FatherRabbit)
