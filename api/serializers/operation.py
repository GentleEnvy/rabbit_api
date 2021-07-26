from rest_framework import serializers

__all__ = ['OperationListSerializer']


class OperationListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.serialize()

    def update(self, instance, validated_data):
        raise AttributeError

    def create(self, validated_data):
        raise AttributeError
