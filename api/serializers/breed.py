from rest_framework import serializers

from api.models import Breed

__all__ = ['BreedListSerializer']


class BreedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'
