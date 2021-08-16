from rest_framework import serializers

from api.models import *

__all__ = ['MotherRabbitPartnerSerializer', 'FatherRabbitPartnerSerializer']


class _BasePartnerSerializer(serializers.Serializer):
    class _PartnerField(serializers.PrimaryKeyRelatedField):
        def __init__(self, **kwargs):
            super().__init__(**kwargs, required=True, allow_null=False, allow_empty=False)
        
        def to_internal_value(self, data):
            partner = super().to_internal_value(data)
            if partner.is_male:
                partner: FatherRabbit
                partner.cleaner.for_mating()
            else:  # partner is female
                partner: MotherRabbit
                partner.cleaner.for_mating()
                partner.cleaner.check_task()
                partner.cleaner.check_womb()
            return partner
    
    partner: _PartnerField
    
    def update(self, instance, validated_data):
        raise AttributeError
    
    def create(self, validated_data):
        raise AttributeError


class MotherRabbitPartnerSerializer(_BasePartnerSerializer):
    partner = _BasePartnerSerializer._PartnerField(queryset=FatherRabbit.objects.all())


class FatherRabbitPartnerSerializer(_BasePartnerSerializer):
    partner = _BasePartnerSerializer._PartnerField(queryset=MotherRabbit.objects.all())
