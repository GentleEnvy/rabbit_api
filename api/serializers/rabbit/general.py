from django.forms import model_to_dict
from django.http import QueryDict
from rest_framework import serializers

from api.models import *

__all__ = [
    'RabbitGeneralSerializer', 'MotherRabbitCreateSerializer',
    'FatherRabbitCreateSerializer'
]


# noinspection PyMethodMayBeStatic
class RabbitGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rabbit
        fields = ['id', 'cage', 'birthday', 'is_male', 'current_type', 'weight', 'status']

    cage = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_cage(self, rabbit):
        return model_to_dict(rabbit.cast.cage, fields=['farm_number', 'number', 'letter'])

    def get_weight(self, rabbit):
        # TODO: add wight for all rabbits
        try:
            return BeforeSlaughterInspection.objects.filter(
                rabbit=rabbit
            ).latest('time').weight
        except BeforeSlaughterInspection.DoesNotExist:
            return None

    def get_status(self, rabbit):
        return rabbit.cast.manager.status


class _BaseReproductionRabbitCreateSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        data = {key: value for key, value in self.initial_data.items()}
        farm_number = data.get('cage__farm_number')
        number = data.get('cage__number')
        letter = data.get('cage__letter')
        if None not in (farm_number, number, letter):
            data['cage'] = Cage.objects.filter(
                farm_number=farm_number, number=number, letter=letter
            ).first().id
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
