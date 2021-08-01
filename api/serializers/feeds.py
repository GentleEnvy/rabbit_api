from rest_framework import serializers

from api.models import CommonFeeds, NursingMotherFeeds

__all__ = ['FatteningFeedsCreateSerializer', 'MotherFeedsCreateSerializer']


class FatteningFeedsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonFeeds
        fields = ['date', 'stocks_field']


class MotherFeedsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NursingMotherFeeds
        fields = ['date', 'stocks_field']
