from rest_framework import serializers

from api.models import Cage

__all__ = ['CageDetailSerializer']


class CageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['status']

    status = serializers.MultipleChoiceField(choices=Cage.STATUS_CHOICES)
