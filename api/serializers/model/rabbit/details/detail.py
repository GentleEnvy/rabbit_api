from rest_framework import serializers

from api.serializers.base import BaseReadOnlyRaiseSerializer
from api.serializers.model.rabbit.base import TypedRabbitSerializerMixin
from api.models import *

__all__ = [
    'FatteningRabbitDetailSerializer', 'BunnyDetailSerializer',
    'MotherRabbitDetailSerializer', 'FatherRabbitDetailSerializer'
]


class _CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['farm_number', 'number', 'letter']


# noinspection PyMethodMayBeStatic
class FatteningRabbitDetailSerializer(
    TypedRabbitSerializerMixin, BaseReadOnlyRaiseSerializer
):
    class Meta(TypedRabbitSerializerMixin.Meta):
        model = FatteningRabbit
        read_only_fields = TypedRabbitSerializerMixin.Meta.fields + [
            'id', 'is_male', 'birthday', 'breed', 'cage', 'status'
        ]
        fields = read_only_fields + ['weight']
        depth = 1
    
    cage = _CageSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title


# noinspection PyMethodMayBeStatic
class BunnyDetailSerializer(TypedRabbitSerializerMixin, BaseReadOnlyRaiseSerializer):
    class Meta(TypedRabbitSerializerMixin.Meta):
        model = FatteningRabbit
        read_only_fields = TypedRabbitSerializerMixin.Meta.fields + [
            'id', 'is_male', 'birthday', 'breed', 'cage', 'status'
        ]
        fields = read_only_fields + ['weight']
        depth = 1
    
    cage = _CageSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title


# noinspection PyMethodMayBeStatic
class _ReproductionRabbitDetailSerializer(
    TypedRabbitSerializerMixin, BaseReadOnlyRaiseSerializer
):
    class Meta(TypedRabbitSerializerMixin.Meta):
        read_only_fields = TypedRabbitSerializerMixin.Meta.fields + [
            'id', 'is_male', 'birthday', 'breed', 'cage', 'status', 'output',
            'output_efficiency'
        ]
        fields = read_only_fields + ['weight']
        depth = 1
    
    cage = _CageSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()
    output_efficiency = serializers.SerializerMethodField()
    
    def get_status(self, rabbit):
        return rabbit.cast.manager.status
    
    def get_breed(self, rabbit):
        return rabbit.breed.title
    
    def get_output(self, rabbit):
        return rabbit.manager.output
    
    def get_output_efficiency(self, rabbit):
        return rabbit.manager.output_efficiency


# noinspection PyMethodMayBeStatic
class MotherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    class Meta(_ReproductionRabbitDetailSerializer.Meta):
        model = MotherRabbit


# noinspection PyMethodMayBeStatic
class FatherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    class Meta(_ReproductionRabbitDetailSerializer.Meta):
        model = FatherRabbit
