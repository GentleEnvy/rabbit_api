from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.fields import SkipField

from api.serializers.base import BaseSupportsCageSerializer
from api.serializers.fields.rabbit import RabbitTypeField
from api.models import *

__all__ = [
    'RabbitListSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitListSerializer(serializers.ModelSerializer):
    # noinspection PyAbstractClass
    class _PlanField(serializers.SerializerMethodField):
        def get_attribute(self, rabbit):
            if isinstance(rabbit.cast, FatteningRabbit):
                return super().get_attribute(rabbit)
            raise SkipField
    
    class Meta:
        model = Rabbit
        fields = [
            'id', 'current_type', 'cage', 'birthday', 'is_male', 'breed', 'plan',
            'weight', 'status'
        ]
    
    cage = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    current_type = RabbitTypeField()
    plan = _PlanField()
    
    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title


class _BaseReproductionRabbitCreateSerializer(BaseSupportsCageSerializer):
    class Meta:
        read_only_fields = ['id']
        fields = read_only_fields + [
            'birthday', 'breed', 'cage', 'is_male', 'is_vaccinated'
        ]
    
    is_vaccinated = serializers.HiddenField(default=True)


class MotherRabbitCreateSerializer(_BaseReproductionRabbitCreateSerializer):
    class Meta(_BaseReproductionRabbitCreateSerializer.Meta):
        model = MotherRabbit
    
    is_male = serializers.HiddenField(default=False)


class FatherRabbitCreateSerializer(_BaseReproductionRabbitCreateSerializer):
    class Meta(_BaseReproductionRabbitCreateSerializer.Meta):
        model = FatherRabbit
    
    is_male = serializers.HiddenField(default=True)
