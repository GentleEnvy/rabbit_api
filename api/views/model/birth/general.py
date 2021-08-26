from api.serializers.birth.general import BirthListSerializer
from api.services.model.rabbit.filterer import RabbitFilterer
from api.services.model.rabbit.managers import MotherRabbitManager
from api.models import *
from api.views.model.base import BaseGeneralView

__all__ = ['BirthConfirmedGeneralView', 'BirthUnconfirmedGeneralView']


class _BaseBirthGeneralView(BaseGeneralView):
    list_serializer = BirthListSerializer
    queryset = MotherRabbit.Manager.prefetch_children(
        MotherRabbit.Manager.prefetch_matings(
            MotherRabbit.Manager.prefetch_bunnies(
                MotherRabbit.Manager.prefetch_pregnancy_inspections(
                    MotherRabbit.objects.all()
                )
            )
        )
    )
    _allow_statuses: list[str]
    
    __BIRTH_TIME_ORDER = 'birth_time'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        
        filterer = RabbitFilterer(queryset)
        filterer.filter(status=self._allow_statuses)
        
        if order := params.get('__order_by__'):
            if order in (self.__BIRTH_TIME_ORDER, f'-{self.__BIRTH_TIME_ORDER}'):
                return self._order_by_birth_time(filterer.queryset, order.startswith('-'))
            return filterer.order_by(order)
        return filterer.queryset
    
    # TODO: to mother rabbit filterer
    @staticmethod
    def _order_by_birth_time(queryset, is_reverse):
        return sorted(
            queryset, key=lambda mr: mr.manager.last_fertilization, reverse=is_reverse
        )


class BirthConfirmedGeneralView(_BaseBirthGeneralView):
    _allow_statuses = [MotherRabbitManager.STATUS_CONFIRMED_PREGNANT]


class BirthUnconfirmedGeneralView(_BaseBirthGeneralView):
    _allow_statuses = [MotherRabbitManager.STATUS_UNCONFIRMED_PREGNANT]
