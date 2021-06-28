from rest_framework.fields import MultipleChoiceField

from api.models import *
from api.serializers.base import BaseModelSerializer

__all__ = ['create_default_retrieve_serializer', 'create_default_update_serializer']


def create_default_retrieve_serializer(serializer_model):
    class DefaultRetrieveSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'

    return DefaultRetrieveSerializer


def create_default_update_serializer(serializer_model):
    class DefaultUpdateSerializer(BaseModelSerializer):
        class Meta:
            model = serializer_model
            fields = '__all__'

        status = MultipleChoiceField(choices=Cage.STATUS_CHOICES)

    return DefaultUpdateSerializer
