from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['InProgressTaskListSerializer']


def _cage_serializer(get_cage):
    def serialize_cage(*args, **kwargs):
        cage = get_cage(*args, **kwargs)
        return model_to_dict(cage, fields=['farm_number', 'number', 'letter'])
    return serialize_cage


# noinspection PyMethodMayBeStatic
class _BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'type', 'created_at', 'user']
    
    type = serializers.SerializerMethodField()
    
    def get_type(self, task):
        return task.CHAR_TYPE


# noinspection PyMethodMayBeStatic
class _CageTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = ToReproductionTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage']
    
    cage = serializers.SerializerMethodField()
    
    @_cage_serializer
    def get_cage(self, task):
        return self._get_cage(task)
    
    def _get_cage(self, task):
        return task.cage


# noinspection PyMethodMayBeStatic
class _ToReproductionTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = ToReproductionTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage_from', 'cage_to']
    
    cage_from = serializers.SerializerMethodField()
    
    @_cage_serializer
    def get_cage_from(self, task):
        return task.rabbit.cage


# noinspection PyMethodMayBeStatic
class _ToFatteningTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = ToFatteningTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage_from', 'cage_to']
    
    cage_from = serializers.SerializerMethodField()
    
    @_cage_serializer
    def get_cage_from(self, task):
        return task.rabbit.cage


class _MatingTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = MatingTask
        fields = _BaseTaskSerializer.Meta.fields + ['cage_from', 'cage_to']
    
    cage_from = serializers.SerializerMethodField()
    cage_to = serializers.SerializerMethodField()
    
    @_cage_serializer
    def get_cage_from(self, task):
        return task.mother_rabbit.cage
    
    @_cage_serializer
    def get_cage_to(self, task):
        return task.father_rabbit.cage


class _BunnyJiggingTaskSerializer(_BaseTaskSerializer):
    class Meta(_BaseTaskSerializer.Meta):
        model = BunnyJiggingTask
        fields = _BaseTaskSerializer.Meta.fields + [
            'cage_from', 'male_cage_to', 'female_cage_to'
        ]
    
    cage_from = serializers.SerializerMethodField()
    male_cage_to = serializers.SerializerMethodField()
    female_cage_to = serializers.SerializerMethodField()
    
    @_cage_serializer
    def get_cage_from(self, task):
        return task.cage_from
    
    @_cage_serializer
    def get_male_cage_to(self, task):
        return task.male_cage_to
    
    @_cage_serializer
    def get_female_cage_to(self, task):
        return task.female_cage_to


class _VaccinationTaskSerializer(_CageTaskSerializer):
    class Meta(_CageTaskSerializer.Meta):
        model = VaccinationTask


class _SlaughterInspectionTaskSerializer(_CageTaskSerializer):
    class Meta(_CageTaskSerializer.Meta):
        model = SlaughterInspectionTask


# noinspection PyMethodMayBeStatic
class _SlaughterTaskSerializer(_CageTaskSerializer):
    class Meta(_CageTaskSerializer.Meta):
        model = SlaughterTask
        fields = _BaseTaskSerializer.Meta.fields + ['weight']
    
    weight = serializers.SerializerMethodField()
    
    def get_weight(self, task):
        return task.rabbit.weight
    
    def _get_cage(self, task):
        return task.rabbit.cast.cage


_model__serializer = {
    serializer.Meta.model: serializer for serializer in (
        _ToReproductionTaskSerializer, _ToFatteningTaskSerializer, _MatingTaskSerializer,
        _BunnyJiggingTaskSerializer, _VaccinationTaskSerializer,
        _SlaughterInspectionTaskSerializer, _SlaughterTaskSerializer
    )
}


# noinspection PyAbstractClass
class InProgressTaskListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return _model__serializer[type(instance)]().to_representation(instance)
