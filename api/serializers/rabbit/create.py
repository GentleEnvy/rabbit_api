from rest_framework.serializers import HiddenField, BooleanField, ModelSerializer

from api.serializers._base import BaseModelSerializer
from api.models import *

__all__ = [
    'FatteningRabbitCreateSerializer', 'BunnyCreateSerializer',
    'MotherRabbitCreateSerializer', 'FatherRabbitCreateSerializer'
]


class FatteningRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = FatteningRabbit
        fields = '__all__'

    current_type = HiddenField(default=FatteningRabbit.CHAR_TYPE)


class BunnyCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Bunny
        fields = '__all__'

    current_type = HiddenField(default=Bunny.CHAR_TYPE)


class MotherRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'

    current_type = HiddenField(default=MotherRabbit.CHAR_TYPE)
    is_male = HiddenField(default=False)


class FatherRabbitCreateSerializer(BaseModelSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'

    current_type = HiddenField(default=FatherRabbit.CHAR_TYPE)
    is_male = HiddenField(default=True)
