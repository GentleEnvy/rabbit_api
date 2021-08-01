from rest_framework import serializers

from api.serializers.cage.default import OnlyNumberCageSerializer
from api.managers import MotherRabbitManager
from api.models import *

__all__ = ['BirthListSerializer']


# noinspection PyMethodMayBeStatic
class BirthListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherRabbit
        fields = ['id', 'cage', 'last_fertilization', 'is_confirmed']
    
    cage = OnlyNumberCageSerializer()
    last_fertilization = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()
    
    def get_last_fertilization(self, rabbit):
        return rabbit.manager.last_fertilization
    
    def get_is_confirmed(self, rabbit):
        mother_status = rabbit.manager.status
        if MotherRabbitManager.STATUS_CONFIRMED_PREGNANT in mother_status:
            return True
        if MotherRabbitManager.STATUS_UNCONFIRMED_PREGNANT in mother_status:
            return False
        raise TypeError('Mother rabbit is not pregnant')
