from rest_framework import serializers
from rest_framework.exceptions import ValidationError

__all__ = ['BaseReadOnlyRaiseSerializer']


class BaseReadOnlyRaiseSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        for field_name, field in self.fields.items():
            if field.read_only and field_name in data:
                raise ValidationError({
                    field_name: f'{field_name} is read only'
                })
        return super().to_internal_value(data)
