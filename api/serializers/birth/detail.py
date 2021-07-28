from rest_framework import serializers

__all__ = ['BirthUnconfirmedDataSerializer', 'BirthConfirmedDataSerializer']


# noinspection PyAbstractClass
class BirthUnconfirmedDataSerializer(serializers.Serializer):
    is_pregnant = serializers.BooleanField(required=True, write_only=True)


# noinspection PyAbstractClass
class BirthConfirmedDataSerializer(serializers.Serializer):
    born_bunnies = serializers.IntegerField(required=True, write_only=True)
