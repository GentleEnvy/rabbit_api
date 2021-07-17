from rest_framework import serializers

from api.models import Plan, FatteningRabbit

__all__ = ['PlanListSerializer']


class PlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    rabbits = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FatteningRabbit.objects.all(), source='fatteningrabbit_set'
    )
