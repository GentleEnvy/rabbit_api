from rest_framework import serializers

__all__ = ['OperationListSerializer']


class OperationListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.serialize()
