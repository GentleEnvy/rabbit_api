from datetime import datetime

from api.managers import MotherRabbitManager
from api.models import *
from api.serializers import *
from api.services.filterers import RabbitFilterer
from api.views.models.base import BaseDetailView

__all__ = ['BirthUnconfirmedDetailView', 'BirthConfirmedDetailView']


class _BaseBirthDetailView(BaseDetailView):
    queryset = MotherRabbit.all_current.all()
    lookup_url_kwarg = 'id'
    filter_status: str
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filterer = RabbitFilterer(queryset)
        filterer.filter(
            status=[self.filter_status]
        )
        return filterer.queryset


class BirthUnconfirmedDetailView(_BaseBirthDetailView):
    filter_status = MotherRabbitManager.STATUS_UNCONFIRMED_PREGNANT
    update_serializer = BirthUnconfirmedDataSerializer
    
    def perform_update(self, serializer):
        PregnancyInspection.objects.create(
            mother_rabbit=serializer.instance, **serializer.validated_data
        )


class BirthConfirmedDetailView(_BaseBirthDetailView):
    filter_status = MotherRabbitManager.STATUS_CONFIRMED_PREGNANT
    update_serializer = BirthConfirmedDataSerializer
    
    def perform_update(self, serializer):
        now = datetime.utcnow()
        mother: MotherRabbit = serializer.instance
        for _ in range(serializer.validated_data['born_bunnies']):
            Bunny.objects.create(
                birthday=now, mother=mother,
                father=mother.manager.last_mating.father_rabbit,
                breed=mother.breed, cage=mother.cage
            )
