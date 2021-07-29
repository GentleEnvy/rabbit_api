from rest_framework import serializers

from api.models import *
from api.serializers.cage.default import OnlyNumberCageSerializer

__all__ = ['AnonymousTaskListSerializer']


# noinspection PyMethodMayBeStatic
class _BaseTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'type', 'created_at']
    
    type = serializers.SerializerMethodField()
    
    def get_type(self, task):
        return task.CHAR_TYPE


# noinspection PyMethodMayBeStatic
class _DefaultTaskListSerializer(_BaseTaskListSerializer):
    class Meta(_BaseTaskListSerializer.Meta):
        fields = _BaseTaskListSerializer.Meta.fields + ['cage']
    
    cage = serializers.SerializerMethodField()
    
    def get_cage(self, task):
        return OnlyNumberCageSerializer().to_representation(self._get_cage(task))
    
    def _get_cage(self, task):
        if isinstance(task, (ToReproductionTask, ToFatteningTask, SlaughterTask)):
            return task.rabbit.cage
        if isinstance(task, BunnyJiggingTask):
            return task.cage_from
        return task.cage


class _MatingTaskListSerializer(_BaseTaskListSerializer):
    class Meta(_BaseTaskListSerializer.Meta):
        fields = _BaseTaskListSerializer.Meta.fields + ['mother_cage', 'father_cage']
    
    mother_cage = OnlyNumberCageSerializer(source='mother_rabbit__cage')
    father_cage = OnlyNumberCageSerializer(source='father_rabbit__cage')


_model__serializer = {
    MatingTask: _MatingTaskListSerializer
}


# noinspection PyAbstractClass
class AnonymousTaskListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        try:
            serializer = _model__serializer[type(instance)]()
        except KeyError:
            serializer = _DefaultTaskListSerializer()
        return serializer.to_representation(instance)
