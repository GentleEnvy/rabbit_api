from django.forms import model_to_dict
from rest_framework import serializers

from api.serializers.base import BaseSupportsCageSerializer
from api.serializers.model.rabbit.base import TypedRabbitSerializerMixin
from api.models import *

__all__ = [
    'RabbitListSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitListSerializer(TypedRabbitSerializerMixin, serializers.ModelSerializer):
    class Meta(TypedRabbitSerializerMixin.Meta):
        model = Rabbit
        fields = TypedRabbitSerializerMixin.Meta.fields + [
            'id', 'cage', 'birthday', 'is_male', 'breed', 'weight', 'status'
        ]
    
    cage = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    
    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title


class MotherRabbitCreateSerializer(
    TypedRabbitSerializerMixin, BaseSupportsCageSerializer
):
    class Meta(TypedRabbitSerializerMixin.Meta):
        model = MotherRabbit
        fields = TypedRabbitSerializerMixin.Meta.fields + [
            'birthday', 'breed', 'cage', 'is_male', 'is_vaccinated'
        ]
    
    is_male = serializers.HiddenField(default=False)
    is_vaccinated = serializers.HiddenField(default=True)


class FatherRabbitCreateSerializer(
    TypedRabbitSerializerMixin, BaseSupportsCageSerializer
):
    class Meta(TypedRabbitSerializerMixin.Meta):
        model = FatherRabbit
        fields = TypedRabbitSerializerMixin.Meta.fields + [
            'birthday', 'breed', 'cage', 'is_male', 'is_vaccinated'
        ]
    
    is_male = serializers.HiddenField(default=True)
    is_vaccinated = serializers.HiddenField(default=True)
