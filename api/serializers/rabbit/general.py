from django.forms import model_to_dict
from rest_framework import serializers

from api.models import *

__all__ = [
    'RabbitListSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = ['id', 'cage', 'birthday', 'is_male', 'current_type', 'weight', 'status']

    cage = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])

    def get_status(self, rabbit):
        return rabbit.cast.manager.status


class _BaseReproductionRabbitCreateSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        data = {key: value for key, value in self.initial_data.items()}
        farm_number = data.get('cage__farm_number')
        number = data.get('cage__number')
        letter = data.get('cage__letter')
        if None not in (farm_number, number, letter):
            data['cage'] = Cage.objects.get(
                farm_number=farm_number, number=number, letter=letter
            ).id
        self.initial_data = data
        return super().is_valid(raise_exception)


class MotherRabbitCreateSerializer(_BaseReproductionRabbitCreateSerializer):
    class Meta:
        model = MotherRabbit
        fields = '__all__'

    current_type = serializers.HiddenField(default=Meta.model.CHAR_TYPE)
    is_male = serializers.HiddenField(default=False)


class FatherRabbitCreateSerializer(_BaseReproductionRabbitCreateSerializer):
    class Meta:
        model = FatherRabbit
        fields = '__all__'

    current_type = serializers.HiddenField(default=Meta.model.CHAR_TYPE)
    is_male = serializers.HiddenField(default=True)
