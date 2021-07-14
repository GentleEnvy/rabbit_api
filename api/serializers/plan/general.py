from rest_framework import serializers

from api.models import Plan

__all__ = ['PlanListSerializer']


class PlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['type', 'quantity', 'date']
