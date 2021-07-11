from rest_framework import serializers

from api.serializers.base import *
from api.models import *

__all__ = ['DeadRabbitRecastSerializer', 'FatteningRabbitRecastSerializer']


class DeadRabbitRecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadRabbit
        fields = ['death_day', 'death_cause']


class FatteningRabbitRecastSerializer(BaseSupportsCageSerializer):
    class Meta:
        model = FatteningRabbit
        fields = ['is_male', 'is_vaccinated', 'weight', 'cage']

    is_male = serializers.BooleanField(required=False)
    weight = serializers.FloatField(required=False)
