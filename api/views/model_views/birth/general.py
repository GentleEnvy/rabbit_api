from api.managers import MotherRabbitManager
from api.models import MotherRabbit
from api.serializers import BirthListSerializer
from api.services.filterers import RabbitFilterer
from api.views.model_views.base import BaseGeneralView

__all__ = ['BirthGeneralView']


class BirthGeneralView(BaseGeneralView):
    list_serializer = BirthListSerializer
    queryset = MotherRabbit.all_current.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filterer = RabbitFilterer(queryset)
        filterer.filter(
            status=[
                MotherRabbitManager.STATUS_CONFIRMED_PREGNANT,
                MotherRabbitManager.STATUS_UNCONFIRMED_PREGNANT
            ]
        )
        return filterer.queryset
