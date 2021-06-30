from rest_framework.serializers import *

from api.serializers.base import BaseModelSerializer

__all__ = ['create_default_retrieve_serializer', 'create_default_create_serializer']


def create_default_retrieve_serializer(
        serializer_model, serializer_depth=0, is_male_field=None
):
    class DefaultRetrieveSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'
            depth = serializer_depth

        current_type = CharField(read_only=True)
        is_male = is_male_field

    return DefaultRetrieveSerializer


def create_default_create_serializer(serializer_model, is_male_field=None):
    class DefaultCreateSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'

        current_type = HiddenField(default=serializer_model.CHAR_TYPE)
        is_male = is_male_field

    return DefaultCreateSerializer
