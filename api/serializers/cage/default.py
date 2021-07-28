from rest_framework import serializers

from api.models import Cage

__all__ = ['OnlyNumberCageSerializer']


class OnlyNumberCageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['farm_number', 'number', 'letter']
