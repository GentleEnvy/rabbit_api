from rest_framework.fields import HiddenField

from api.models import *
from api.serializers.base import BaseModelSerializer
from api.views.model_views.base import BaseGeneralView
from api.views.model_views.rabbit._default_serializers import \
    create_default_retrieve_serializer

__all__ = [
    'RabbitGeneralView', 'DeadRabbitGeneralView', 'FatteningRabbitGeneralView',
    'BunnyGeneralView', 'MotherRabbitGeneralView', 'FatherRabbitGeneralView'
]


def _create_default_create_serializer(serializer_model, is_male_field=None):
    if is_male_field is None:
        class DefaultCreateSerializer(BaseModelSerializer):
            class Meta:
                model = serializer_model
                fields = '__all__'

            current_type = HiddenField(default=serializer_model.CHAR_TYPE)
    else:
        class DefaultCreateSerializer(BaseModelSerializer):
            class Meta:
                model = serializer_model
                fields = '__all__'

            current_type = HiddenField(default=serializer_model.CHAR_TYPE)
            is_male = is_male_field

    return DefaultCreateSerializer


class RabbitGeneralView(BaseGeneralView):
    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = Rabbit
            fields = '__all__'

    model = Rabbit
    list_serializer = __ListSerializer


class DeadRabbitGeneralView(BaseGeneralView):
    model = DeadRabbit
    list_serializer = create_default_retrieve_serializer(model)


class FatteningRabbitGeneralView(BaseGeneralView):
    model = FatteningRabbit
    create_serializer = _create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)


class BunnyGeneralView(BaseGeneralView):
    model = Bunny
    create_serializer = _create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)


class MotherRabbitGeneralView(BaseGeneralView):
    model = MotherRabbit
    create_serializer = _create_default_create_serializer(
        model, is_male_field=HiddenField(default=False)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)


class FatherRabbitGeneralView(BaseGeneralView):
    model = FatherRabbit
    create_serializer = _create_default_create_serializer(
        model, is_male_field=HiddenField(default=True)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)
