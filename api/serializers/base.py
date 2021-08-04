from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Cage

__all__ = ['EmptySerializer', 'BaseReadOnlyRaiseSerializer', 'BaseSupportsCageSerializer']


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []


class BaseReadOnlyRaiseSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        for field_name, field in self.fields.items():
            if field.read_only and field_name in data:
                raise ValidationError(
                    {
                        field_name: f'{field_name} is read only'
                    }
                )
        return super().to_internal_value(data)


# TODO: replace to a custom Field (OnlyNumberCageField) instead of a Serializer
class BaseSupportsCageSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        data = {key: value for key, value in self.initial_data.items()}
        farm_number = data.pop('cage__farm_number', None)
        number = data.pop('cage__number', None)
        letter = data.pop('cage__letter', None)
        if None not in (farm_number, number, letter):
            data['cage'] = Cage.objects.get(
                farm_number=farm_number, number=number, letter=letter
            ).cast
        self.initial_data = data
        return super().is_valid(raise_exception)
