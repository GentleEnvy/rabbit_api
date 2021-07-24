from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['AnonymousTaskListSerializer']


def _get_cage(cage: Cage):
    model_to_dict(cage, fields=['farm_number', 'number', 'letter'])


# noinspection PyMethodMayBeStatic
class _BaseTaskSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    
    def get_type(self, task):
        return task.CHAR_TYPE


# noinspection PyMethodMayBeStatic
class ToReproductionTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = ToReproductionTask
        fields = '__all__'
    
    cage_to = serializers.SerializerMethodField()
    
    def get_cage_to(self, task):
        return _get_cage(task.cage_to)


class SlaughterTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = SlaughterTask
        fields = '__all__'


class MatingTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = MatingTask
        fields = '__all__'


# noinspection PyMethodMayBeStatic
class BunnyJiggingTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = BunnyJiggingTask
        fields = '__all__'


# noinspection PyMethodMayBeStatic
class VaccinationTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = VaccinationTask
        fields = '__all__'
    
    cage = serializers.SerializerMethodField()
    
    def get_cage(self, task):
        return _get_cage(task.cage)


class SlaughterInspectionTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = SlaughterInspectionTask
        fields = '__all__'


class FatteningSlaughterTaskSerializer(_BaseTaskSerializer):
    class Meta:
        model = FatteningSlaughterTask
        fields = '__all__'


_model__serializer = {
    serializer.Meta.model: serializer for serializer in (
        ToReproductionTaskSerializer, SlaughterTaskSerializer, MatingTaskSerializer,
        BunnyJiggingTaskSerializer, VaccinationTaskSerializer,
        SlaughterInspectionTaskSerializer, FatteningSlaughterTaskSerializer
    )
}


class AnonymousTaskListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return _model__serializer[type(instance)]().to_representation(instance)
    
    def update(self, instance, validated_data):
        raise AttributeError
    
    def create(self, validated_data):
        raise AttributeError
