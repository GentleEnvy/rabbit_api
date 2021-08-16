from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.models import *
from api.serializers.model.rabbit.generals.death import RabbitDeathSerializer
from api.views.base import BaseView

__all__ = ['RabbitDeathView']


class RabbitDeathView(BaseView):
    serializer_class = RabbitDeathSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            try:
                for error_detail in e.detail['cage']:
                    if getattr(error_detail, 'code') == 'does_not_exist':
                        raise APIWarning(e.detail, codes=['death', 'cage_not_exist'])
            except KeyError:
                raise e
            raise e
        cage = serializer.validated_data['cage']
        death_cause = serializer.validated_data['death_cause']
        
        rabbits = list(cage.manager.rabbits)
        if len(rabbits) == 0:
            raise APIWarning(
                'There are no rabbits in this cage', codes=['death', 'not_rabbits']
            )
        
        if death_cause == DeadRabbit.CAUSE_ILLNESS:
            for sick_rabbit in cage.manager.rabbits:
                self._die(sick_rabbit, DeadRabbit.CAUSE_ILLNESS)
        elif death_cause == DeadRabbit.CAUSE_MOTHER:
            self._death_by_mother(cage)
        elif cage.CHAR_TYPE == MotherCage.CHAR_TYPE:
            rabbit = cage.bunny_set.first()
            if rabbit is None:
                self._die(cage.manager.rabbits[0], death_cause)
            else:
                self._die(rabbit, death_cause)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def _death_by_mother(self, cage):
        if cage.CHAR_TYPE != MotherCage.CHAR_TYPE:
            raise APIWarning(
                'This cage is not a MotherCage', codes=['death', 'not_mother_cage']
            )
        bunny = cage.bunny_set.first()
        if bunny is None:
            raise APIWarning(
                'In this cage there is no bunnies', codes=['death', 'not_bunnies']
            )
        self._die(bunny, DeadRabbit.CAUSE_MOTHER)
    
    @staticmethod
    def _die(rabbit, cause) -> DeadRabbit:
        dead_rabbit = DeadRabbit.recast(rabbit)
        dead_rabbit.death_cause = cause
        dead_rabbit.save()
        return dead_rabbit
