from django.db.models import Count
from rest_framework import serializers

from api.models import *
from api.serializers.fields import CageByNumberField

__all__ = ['RabbitDeathSerializer']

# noinspection SpellCheckingInspection
_cage_rabbits = (
    'fatteningcage__fatteningrabbit', 'fatteningcage__fatherrabbit',
    'mothercage__motherrabbit', 'mothercage__bunny'
)


class RabbitDeathSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadRabbit
        fields = ['cage', 'death_cause']
    
    cage = CageByNumberField(
        queryset=Cage.objects.select_subclasses().prefetch_related(
            *map(lambda s: s + '_set', _cage_rabbits)
        ).annotate(rabbits__count=sum(map(Count, _cage_rabbits))).exclude(
            rabbits__count=0
        )
    )
