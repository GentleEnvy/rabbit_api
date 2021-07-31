from api.managers import MotherRabbitManager
from api.models import MotherRabbit
from api.serializers import BirthListSerializer
from api.services.filterers import RabbitFilterer
from api.views.model_views.base import BaseGeneralView

__all__ = ['BirthConfirmedGeneralView', 'BirthUnconfirmedGeneralView']


class _BaseBirthGeneralView(BaseGeneralView):
    list_serializer = BirthListSerializer
    queryset = MotherRabbit.all_current.all()
    _allow_statuses: list[str]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filterer = RabbitFilterer(queryset)
        filterer.filter(status=self._allow_statuses)
        return filterer.queryset


class BirthConfirmedGeneralView(_BaseBirthGeneralView):
    _allow_statuses = [MotherRabbitManager.STATUS_CONFIRMED_PREGNANT]


class BirthUnconfirmedGeneralView(_BaseBirthGeneralView):
    _allow_statuses = [MotherRabbitManager.STATUS_UNCONFIRMED_PREGNANT]
