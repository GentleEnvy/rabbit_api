from rest_framework.serializers import *

from api.serializers.base import BaseModelSerializer

__all__ = ['create_default_retrieve_serializer']


def create_default_retrieve_serializer(serializer_model, serializer_depth=0):
    class DefaultRetrieveSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'
            depth = serializer_depth

        current_type = CharField(read_only=True)

    return DefaultRetrieveSerializer
