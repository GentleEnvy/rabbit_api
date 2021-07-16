from rest_framework import serializers

from api.models import Cage

__all__ = ['CageUpdateSerializer']


class CageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['status']

    status = serializers.MultipleChoiceField(choices=Cage.STATUS_CHOICES)
