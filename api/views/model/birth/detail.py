from datetime import datetime

from api.serializers.birth.detail import *
from api.services.model.rabbit.filterer import RabbitFilterer
from api.services.model.rabbit.managers import MotherRabbitManager
from api.models import *
from api.views.model.base import BaseDetailView

__all__ = ['BirthUnconfirmedDetailView', 'BirthConfirmedDetailView']


class _BaseBirthDetailView(BaseDetailView):
    queryset = MotherRabbit.objects.all()
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
