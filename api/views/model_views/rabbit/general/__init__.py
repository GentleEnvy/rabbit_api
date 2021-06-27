from rest_framework.fields import HiddenField

from api.models import *
from api.serializers.base import BaseModelSerializer
from api.views.model_views.rabbit.general.base import BaseRabbitGeneralView

__all__ = [
    'DeadRabbitGeneralView', 'FatteningRabbitGeneralView', 'BunnyGeneralView',
    'MotherRabbitGeneralView', 'FatherRabbitGeneralView'
]


class RabbitGeneralView(BaseRabbitGeneralView):
    pass


class DeadRabbitGeneralView(BaseRabbitGeneralView):
    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = DeadRabbit
            exclude = ['current_type']

    model = DeadRabbit
    list_serializer = __ListSerializer


class FatteningRabbitGeneralView(BaseRabbitGeneralView):
    class __CreateSerializer(BaseModelSerializer):
        class Meta:
            model = FatteningRabbit
            fields = '__all__'

        current_type = HiddenField(default=FatteningRabbit.CHAR_TYPE)

    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = FatteningRabbit
            exclude = ['current_type']
            depth = 1

    model = FatteningRabbit
    create_serializer = __CreateSerializer
    list_serializer = __ListSerializer


class BunnyGeneralView(BaseRabbitGeneralView):
    class __CreateSerializer(BaseModelSerializer):
        class Meta:
            model = Bunny
            fields = '__all__'

        current_type = HiddenField(default=Bunny.CHAR_TYPE)

    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = Bunny
            exclude = ['current_type']
            depth = 1

    model = Bunny
    create_serializer = __CreateSerializer
    list_serializer = __ListSerializer


class MotherRabbitGeneralView(BaseRabbitGeneralView):
    class __CreateSerializer(BaseModelSerializer):
        class Meta:
            model = MotherRabbit
            fields = '__all__'

        current_type = HiddenField(default=MotherRabbit.CHAR_TYPE)
        is_male = HiddenField(default=False)

    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = MotherRabbit
            exclude = ['current_type']
            depth = 1

    model = MotherRabbit
    create_serializer = __CreateSerializer
    list_serializer = __ListSerializer


class FatherRabbitGeneralView(BaseRabbitGeneralView):
    class __CreateSerializer(BaseModelSerializer):
        class Meta:
            model = FatherRabbit
            fields = '__all__'

        current_type = HiddenField(default=FatherRabbit.CHAR_TYPE)
        is_male = HiddenField(default=True)

    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = FatherRabbit
            exclude = ['current_type']
            depth = 1

    model = FatherRabbit
    create_serializer = __CreateSerializer
    list_serializer = __ListSerializer
