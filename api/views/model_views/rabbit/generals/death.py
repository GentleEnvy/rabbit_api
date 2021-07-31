from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from api.models import *
from api.serializers import RabbitDeathSerializer
from api.views.base import BaseView

__all__ = ['RabbitDeathView']


# noinspection PyMethodMayBeStatic
class RabbitDeathView(BaseView):
    serializer_class = RabbitDeathSerializer
    
    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cage = serializer.validated_data['cage']
        death_cause = serializer.validated_data['death_cause']
        
        rabbit = None
        if death_cause == DeadRabbit.CAUSE_ILLNESS:
            for sick_rabbit in cage.rabbits:
                self._die(sick_rabbit, DeadRabbit.CAUSE_ILLNESS)
        elif death_cause == DeadRabbit.CAUSE_MOTHER:
            self._death_by_mother(cage)
        elif cage.CHAR_TYPE == MotherCage.CHAR_TYPE:
            rabbit = cage.bunny_set.first()
        
        if rabbit is None:
            rabbit = next(iter(cage.rabbits))
        self._die(rabbit, death_cause)
        
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        if settings.DEBUG:
            return self.delete(request)
        self.http_method_not_allowed(request)
    
    def _death_by_mother(self, cage):
        if cage.CHAR_TYPE != MotherCage.CHAR_TYPE:
            raise ValidationError('This cage is not a MotherCage')
        bunny = cage.bunny_set.first()
        if bunny is None:
            raise ValidationError('In this cage there is no bunnies')
        self._die(bunny, DeadRabbit.CAUSE_MOTHER)
    
    def _die(self, rabbit, cause) -> DeadRabbit:
        dead_rabbit = DeadRabbit.recast(rabbit)
        dead_rabbit.death_cause = cause
        dead_rabbit.save()
        return dead_rabbit
