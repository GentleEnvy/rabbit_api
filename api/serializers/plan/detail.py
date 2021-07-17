from rest_framework import serializers

from api.models import Plan, FatteningRabbit

__all__ = ['PlanUpdateSerializer']


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['rabbits']

    rabbits = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FatteningRabbit.objects.all(), source='fatteningrabbit_set'
    )
