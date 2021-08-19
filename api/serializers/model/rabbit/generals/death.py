from rest_framework import serializers

from api.models import *
from api.serializers.fields import CageByNumberField

__all__ = ['RabbitDeathSerializer']


class RabbitDeathSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadRabbit
        fields = ['cage', 'death_cause']
    
    cage = CageByNumberField(queryset=Cage.Manager.prefetch_rabbits())
