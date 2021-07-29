from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Cage

__all__ = ['BaseReadOnlyRaiseSerializer', 'BaseSupportsCageSerializer']


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


# FIXME: make a custom Field instead of a Serializer
class BaseSupportsCageSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        data = {key: value for key, value in self.initial_data.items()}
        farm_number = data.pop('cage__farm_number', None)
        number = data.pop('cage__number', None)
        letter = data.pop('cage__letter', None)
        if None not in (farm_number, number, letter):
            data['cage'] = Cage.objects.get(
                farm_number=farm_number, number=number, letter=letter
            ).cast  # TODO: select_related
        self.initial_data = data
        return super().is_valid(raise_exception)
