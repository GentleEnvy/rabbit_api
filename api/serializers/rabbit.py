from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['RabbitGeneralSerializer']


class RabbitGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = ['id', 'cage', 'age']

    age = serializers.SerializerMethodField()
    cage = serializers.SerializerMethodField()

    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])

    def get_age(self, rabbit):
        return rabbit.cast.manager.age
