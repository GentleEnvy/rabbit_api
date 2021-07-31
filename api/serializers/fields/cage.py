from rest_framework import serializers

from api.models import Cage

__all__ = ['CageByNumberField']


class CageByNumberField(serializers.PrimaryKeyRelatedField):
    def __init__(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = Cage.objects.select_subclasses()
        super().__init__(**kwargs, queryset=queryset)
    
    def to_internal_value(self, data):
        if isinstance(data, dict):
            farm_number = data.pop('farm_number', None)
            number = data.pop('number', None)
            letter = data.pop('letter', None)
            if None not in (farm_number, number, letter):
                try:
                    data = Cage.objects.get(
                        farm_number=farm_number, number=number, letter=letter
                    ).id
                except Cage.DoesNotExist:
                    self.fail(
                        'does_not_exist', pk_value={
                            'farm_number': farm_number, 'number': number, 'letter': letter
                        }
                    )
        return super().to_internal_value(data)
