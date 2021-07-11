from api.serializers.base import BaseReadOnlyRaiseSerializer
from api.models import DeadRabbit

__all__ = ['DeadRabbitRecastSerializer']


class DeadRabbitRecastSerializer(BaseReadOnlyRaiseSerializer):
    class Meta:
        model = DeadRabbit
        fields = ['death_day', 'death_cause']
