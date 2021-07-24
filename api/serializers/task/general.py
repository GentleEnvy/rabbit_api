from rest_framework import serializers

__all__ = ['TaskListSerializer']


class TaskListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {'type': str(type(instance))}  # FIXME
    
    def update(self, instance, validated_data):
        raise AttributeError
    
    def create(self, validated_data):
        raise AttributeError
