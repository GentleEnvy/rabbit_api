from rest_framework.response import Response

from api.managers import FatteningRabbitManager, MotherRabbitManager, FatherRabbitManager
from api.models import *
from api.views.base import BaseView

__all__ = ['StatisticView']


class StatisticView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        READY_TO_SLAUGHTER = FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER
        MOTHER_READY = MotherRabbitManager.STATUS_READY_FOR_FERTILIZATION
        FATHER_READY = FatherRabbitManager.STATUS_READY_FOR_FERTILIZATION

        rabbits = Rabbit.objects.exclude(current_type=DeadRabbit.CHAR_TYPE).count()
        cages = Cage.objects.count()
        bunnies = Bunny.objects.filter(current_type=Bunny.CHAR_TYPE).count()
        # TODO: operations
        ready_to_slaughter = 0
        for fattening_rabbit in FatteningRabbit.objects.filter(
                current_type=FatteningRabbit.CHAR_TYPE
        ):
            if READY_TO_SLAUGHTER in fattening_rabbit.manager.status:
                ready_to_slaughter += 1
        reproducible_mothers = 0
        for mother_rabbit in MotherRabbit.objects.filter(
                current_type=MotherRabbit.CHAR_TYPE
        ):
            if MOTHER_READY in mother_rabbit.manager.status:
                reproducible_mothers += 1
        reproducible_fathers = 0
        for father_rabbit in FatherRabbit.objects.filter(
                current_type=FatteningRabbit.CHAR_TYPE
        ):
            if FATHER_READY in father_rabbit.manager.status:
                reproducible_fathers += 1
        return Response({
            'rabbits': rabbits,
            'cages': cages,
            'bunnies': bunnies,
            'ready_to_slaughter': ready_to_slaughter,
            'reproducible_mothers': reproducible_mothers,
            'reproducible_fathers': reproducible_fathers
        })