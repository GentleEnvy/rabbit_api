from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = ['AnonymousTaskListSerializer']


# noinspection PyMethodMayBeStatic
class AnonymousTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'type', 'created_at', 'cage']
    
    type = serializers.SerializerMethodField()
    cage = serializers.SerializerMethodField()
    
    def get_type(self, task):
        return task.CHAR_TYPE
    
    def get_cage(self, task):
        return model_to_dict(
            self._get_cage(task), fields=['farm_number', 'number', 'letter']
        )
    
    def _get_cage(self, task):
        if isinstance(task, (ToReproductionTask, ToFatteningTask, SlaughterTask)):
            return task.rabbit.cage
        if isinstance(task, MatingTask):
            return task.mother_rabbit.cage  # MAYBE: task.father_rabbit.cage
        if isinstance(task, BunnyJiggingTask):
            return task.cage_from
        return task.cage
