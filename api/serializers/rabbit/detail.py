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
class MotherRabbitDetailSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        model = Bunny
        read_only_fields = [
            'id', 'is_male', 'birthday', 'breed', 'current_type', 'cage', 'status'
        ]
        fields = read_only_fields + ['weight']
        depth = 1

    cage = _CageSerializer()
    status = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    output = serializers.SerializerMethodField()

    def get_status(self, rabbit):
        return rabbit.cast.manager.status

    def get_breed(self, rabbit):
        return rabbit.breed.title

    def get_output(self, rabbit: MotherRabbit):
        children = rabbit.rabbit_set
        if len(children) == 0:
            return 0
        births = [children[0]]
        for child in children[1:]:
            for birth in births:
                if abs(diff_time(birth, child.birthday).days) > 2:
                    births.append(child.birthday)
                    break
        return len(births)


# noinspection PyMethodMayBeStatic
class FatherRabbitDetailSerializer(BaseReadOnlyRaiseSerializer):
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
    output = serializers.SerializerMethodField()

    def get_status(self, rabbit):
        return rabbit.cast.manager.status

    def get_breed(self, rabbit):
        return rabbit.breed.title

    def get_output(self, rabbit: FatherRabbit):
        children = rabbit.rabbit_set
        if len(children) == 0:
            return 0
        births = [children[0]]
        for child in children[1:]:
            for birth in births:
                if abs(diff_time(birth, child.birthday).days) > 2:
                    births.append(child.birthday)
                    break
        return len(births)
