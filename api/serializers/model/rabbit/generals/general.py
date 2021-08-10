from django.forms import model_to_dict
from rest_framework import serializers

from api.serializers.base import BaseSupportsCageSerializer
from api.serializers.fields.rabbit import RabbitTypeField
from api.models import *

__all__ = [
    'RabbitListSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = [
            'id', 'cage', 'birthday', 'is_male', 'breed', 'weight', 'status',
            'current_type'
        ]
    
    cage = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    current_type = RabbitTypeField()
    
    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title


class _BaseReproductionRabbitCreateSerializer(BaseSupportsCageSerializer):
    class Meta:
        fields = ['birthday', 'breed', 'cage', 'is_male', 'is_vaccinated']
    
    is_vaccinated = serializers.HiddenField(default=True)


class MotherRabbitCreateSerializer(_BaseReproductionRabbitCreateSerializer):
    class Meta(_BaseReproductionRabbitCreateSerializer.Meta):
        model = MotherRabbit
    
    is_male = serializers.HiddenField(default=False)


class FatherRabbitCreateSerializer(BaseSupportsCageSerializer):
    class Meta(_BaseReproductionRabbitCreateSerializer.Meta):
        model = FatherRabbit
    
    is_male = serializers.HiddenField(default=True)
