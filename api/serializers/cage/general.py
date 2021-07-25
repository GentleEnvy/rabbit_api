from rest_framework import serializers
from rest_framework.fields import SkipField

from api.models import *

__all__ = ['CageListSerializer']


# noinspection PyMethodMayBeStatic
class CageListSerializer(serializers.ModelSerializer):
    # noinspection PyAbstractClass
    class _IsParallelField(serializers.SerializerMethodField):
        def get_attribute(self, cage):
            if cage.cast.CHAR_TYPE != MotherCage.CHAR_TYPE:
                raise SkipField
            return super().get_attribute(cage)
    
    class Meta:
        model = Cage
        fields = [
            'id', 'farm_number', 'number', 'letter', 'type', 'is_parallel',
            'number_rabbits', 'status'
        ]
    
    number_rabbits = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    is_parallel = _IsParallelField()
    
    def get_number_rabbits(self, cage):
        return len(cage.cast.rabbits)
    
    def get_type(self, cage):
        return cage.cast.CHAR_TYPE
    
    def get_is_parallel(self, cage):
        return cage.cast.manager.is_parallel
