from django.db.models import Q
from rest_framework import serializers

from api.serializers.base import BaseReadOnlyRaiseSerializer
from api.models import *

__all__ = [
    'FatteningRabbitDetailSerializer', 'BunnyDetailSerializer',
    'MotherRabbitDetailSerializer', 'FatherRabbitDetailSerializer'
]

from api.utils.functions import diff_time


class _CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = ['farm_number', 'number', 'letter']


# noinspection PyMethodMayBeStatic
class FatteningRabbitDetailSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        model = FatteningRabbit
        read_only_fields = [
            'id', 'is_male', 'birthday', 'breed', 'current_type', 'cage', 'status'
        ]
        fields = read_only_fields + ['weight']
        depth = 1

    cage = _CageSerializer()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()

    def get_status(self, rabbit):
        return rabbit.cast.manager.status

    def get_breed(self, rabbit):
        return rabbit.breed.title


# noinspection PyMethodMayBeStatic
class BunnyDetailSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        model = FatteningRabbit
        read_only_fields = [
            'id', 'is_male', 'birthday', 'breed', 'current_type', 'cage', 'status'
        ]
        fields = read_only_fields + ['weight']
        depth = 1

    cage = _CageSerializer()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()

    def get_status(self, rabbit):
        return rabbit.cast.manager.status

    def get_breed(self, rabbit):
        return rabbit.breed.title


# noinspection PyMethodMayBeStatic
class _ReproductionRabbitDetailSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        model = Bunny
        read_only_fields = [
            'id', 'is_male', 'birthday', 'breed', 'current_type', 'cage', 'status',
            'output', 'output_efficiency'
        ]
        fields = read_only_fields + ['weight']
        depth = 1

    cage = _CageSerializer()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()
    output_efficiency = serializers.SerializerMethodField()

    def get_status(self, rabbit):
        return rabbit.cast.manager.status

    def get_breed(self, rabbit):
        return rabbit.breed.title

    def get_output(self, rabbit):
        children = rabbit.rabbit_set.all()
        if len(children) == 0:
            return 0
        births = [children[0].birthday]
        for child in children[1:]:
            for birth in births:
                if abs(diff_time(birth, child.birthday).days) > 2:
                    births.append(child.birthday)
                    break
        return len(births)

    def get_output_efficiency(self, rabbit):
        raise NotImplementedError


# TODO: clarify death_causes
# noinspection PyMethodMayBeStatic
class MotherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    def get_output_efficiency(self, rabbit):
        efficiency_children = rabbit.rabbit_set.filter(
            Q(current_type=FatteningRabbit.CHAR_TYPE) |
            Q(current_type=DeadRabbit.CHAR_TYPE) &
            ~Q(deadrabbit__death_cause=DeadRabbit.CAUSE_MOTHER)
        ).count()
        output = self.get_output(rabbit)
        if output == 0:
            return None
        return efficiency_children / self.get_output(rabbit)


# noinspection PyMethodMayBeStatic
class FatherRabbitDetailSerializer(_ReproductionRabbitDetailSerializer):
    def get_output_efficiency(self, rabbit):
        efficiency_children = rabbit.rabbit_set.filter(
            Q(current_type=FatteningRabbit.CHAR_TYPE) |
            Q(current_type=DeadRabbit.CHAR_TYPE)
        ).count()
        output = self.get_output(rabbit)
        if output == 0:
            return None
        return efficiency_children / self.get_output(rabbit)
