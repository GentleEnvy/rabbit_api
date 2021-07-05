from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['RabbitGeneralSerializer']


# noinspection PyMethodMayBeStatic
class RabbitGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = ['id', 'cage', 'birthday', 'is_male', 'current_type', 'weight', 'status']

    cage = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])

    def get_weight(self, rabbit):
        try:
            return BeforeSlaughterInspection.objects.filter(
                rabbit=rabbit
            ).latest('time').weight
        except BeforeSlaughterInspection.DoesNotExist:
            return None

    def get_status(self, rabbit):
        return rabbit.cast.manager.status
