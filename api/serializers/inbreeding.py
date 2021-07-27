from rest_framework import serializers

__all__ = ['InbreedingDataSerializer']


class InbreedingDataSerializer(serializers.Serializer):
    rabbits = serializers.ListField(
        child=serializers.IntegerField(), required=True, allow_null=False,
        allow_empty=False
    )
    
    def update(self, instance, validated_data):
        raise AttributeError
    
    def create(self, validated_data):
        raise AttributeError
