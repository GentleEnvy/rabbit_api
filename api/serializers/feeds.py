from rest_framework import serializers

from api.models import *

__all__ = ['FatteningFeedsCreateSerializer', 'MotherFeedsCreateSerializer']


class FatteningFeedsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatteningFeeds
        fields = ['time', 'stocks']


class MotherFeedsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherFeeds
        fields = ['time', 'stocks']
