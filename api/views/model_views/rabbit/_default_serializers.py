from rest_framework.serializers import *

from api.models import Cage
from api.serializers.base import BaseModelSerializer

__all__ = ['create_default_retrieve_serializer', 'create_default_create_serializer']


def create_default_retrieve_serializer(
        serializer_model, is_male_field=None
):
    class CageSerializer(BaseModelSerializer):
        class Meta:
            model = Cage
            fields = '__all__'

    class DefaultRetrieveSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'

        current_type = CharField(read_only=True)
        is_male = is_male_field
        cage = CageSerializer()

    return DefaultRetrieveSerializer


def create_default_create_serializer(serializer_model, is_male_field=None):
    class DefaultCreateSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'

        current_type = HiddenField(default=serializer_model.CHAR_TYPE)
        is_male = is_male_field

    return DefaultCreateSerializer
