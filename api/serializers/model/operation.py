from rest_framework import serializers

__all__ = ['OperationListSerializer']


# noinspection PyAbstractClass
class OperationListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.serialize()
