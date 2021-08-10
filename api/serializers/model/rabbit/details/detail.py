from datetime import datetime

from rest_framework import serializers

from api.serializers.base import BaseReadOnlyRaiseSerializer
from api.serializers.fields.rabbit import RabbitTypeField
from api.models import *

__all__ = [
    'FatteningRabbitDetailSerializer', 'BunnyDetailSerializer',
    'MotherRabbitDetailSerializer', 'FatherRabbitDetailSerializer'
]


class _CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['farm_number', 'number', 'letter']


# noinspection PyMethodMayBeStatic
class _BaseRabbitDetailSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        read_only_fields = [
            'id', 'current_type', 'is_male', 'birthday', 'breed', 'cage', 'status',
            'last_weighting'
        ]
        fields = read_only_fields + ['weight']
        depth = 1
    
    cage = _CageSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    current_type = RabbitTypeField()
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title
    
    def save(self, **kwargs):
        self.validated_data['last_weighting'] = datetime.utcnow()
        super().save()


class FatteningRabbitDetailSerializer(_BaseRabbitDetailSerializer):
    class Meta(_BaseRabbitDetailSerializer.Meta):
        model = FatteningRabbit


class BunnyDetailSerializer(_BaseRabbitDetailSerializer):
    class Meta(_BaseRabbitDetailSerializer.Meta):
        model = Bunny


# noinspection PyMethodMayBeStatic
class _ReproductionRabbitDetailSerializer(_BaseRabbitDetailSerializer):
    class Meta(_BaseRabbitDetailSerializer.Meta):
        read_only_fields = _BaseRabbitDetailSerializer.Meta.read_only_fields + [
            'output', 'output_efficiency'
        ]
        fields = read_only_fields + ['weight']
    
    output = serializers.SerializerMethodField()
    output_efficiency = serializers.SerializerMethodField()
    
    def get_output(self, rabbit):
        return rabbit.manager.output
    
    def get_output_efficiency(self, rabbit):
        return rabbit.manager.output_efficiency


# noinspection PyMethodMayBeStatic
class MotherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    class Meta(_ReproductionRabbitDetailSerializer.Meta):
        model = MotherRabbit


# noinspection PyMethodMayBeStatic
class FatherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    class Meta(_ReproductionRabbitDetailSerializer.Meta):
        model = FatherRabbit
