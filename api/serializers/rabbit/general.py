from django.forms import model_to_dict
from rest_framework import serializers

from api.serializers.base import BaseSupportsCageSerializer
from api.models import *

__all__ = [
    'RabbitListSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = ['id', 'cage', 'birthday', 'is_male', 'current_type', 'weight', 'status']

    cage = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])

    def get_status(self, rabbit):
        return rabbit.cast.manager.status


class MotherRabbitCreateSerializer(BaseSupportsCageSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'

    current_type = serializers.HiddenField(default=Meta.model.CHAR_TYPE)
    is_male = serializers.HiddenField(default=False)


class FatherRabbitCreateSerializer(BaseSupportsCageSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'

    current_type = serializers.HiddenField(default=Meta.model.CHAR_TYPE)
    is_male = serializers.HiddenField(default=True)
