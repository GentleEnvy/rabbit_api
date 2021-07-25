from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['AnonymousTaskListSerializer']


def _get_cage(cage: Cage):
    return model_to_dict(cage, fields=['farm_number', 'number', 'letter'])


# noinspection PyMethodMayBeStatic
class _BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'type', 'created_at']
    
    type = serializers.SerializerMethodField()
    
    def get_type(self, task):
        return task.CHAR_TYPE


class ToReproductionTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = ToReproductionTask


class SlaughterTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = SlaughterTask


class MatingTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = MatingTask


# noinspection PyMethodMayBeStatic
class BunnyJiggingTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = BunnyJiggingTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage_from']
    
    cage_from = serializers.SerializerMethodField()
    
    def get_cage_from(self, task):
        return _get_cage(task.cage_from)


# noinspection PyMethodMayBeStatic
class VaccinationTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = VaccinationTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage']
    
    cage = serializers.SerializerMethodField()
    
    def get_cage(self, task):
        return _get_cage(task.cage)


# noinspection PyMethodMayBeStatic
class SlaughterInspectionTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = SlaughterInspectionTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage']
    
    cage = serializers.SerializerMethodField()
    
    def get_cage(self, task):
        return _get_cage(task.cage)


# noinspection PyMethodMayBeStatic
class FatteningSlaughterTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = FatteningSlaughterTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage']
    
    cage = serializers.SerializerMethodField()
    
    def get_cage(self, task):
        return _get_cage(task.cage)


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
