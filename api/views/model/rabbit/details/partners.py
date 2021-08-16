from typing import Optional

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.models import *
from api.serializers.model.rabbit.details.partners import *
from api.services.inbreeding import AvoidInbreedingService
from api.views.base import BaseView

__all__ = ['MotherRabbitPartnersView', 'FatherRabbitPartnersView']


def _find_optimal_partners(rabbit: Rabbit) -> dict[int, Optional[int]]:
    avoid_inbreeding_service = AvoidInbreedingService()
    optimal_partners = avoid_inbreeding_service.find_optimal_partners(rabbit)
    return {
        partner: kinship if kinship != float('inf') else None
        for partner, kinship in optimal_partners.items()
    }


class _BasePartnersView(BaseView):
    lookup_url_kwarg = 'id'
    
    def get(self, request, **_):
        rabbit = self.get_object()
        self._clean(rabbit)
        optimal_partners = _find_optimal_partners(rabbit)
        return Response(optimal_partners)
    
    def post(self, request, **_):
        rabbit = self.get_object()
        rabbit.cleaner.for_mating()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partner = serializer.validated_data['partner']
        self._create_task(rabbit, partner)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def _clean(rabbit):
        try:
            rabbit.cleaner.for_mating()
        except ValidationError as e:
            raise APIWarning(str(e), codes=['mating'])
        if not rabbit.is_male:
            rabbit: MotherRabbit
            try:
                rabbit.cleaner.check_task()
            except ValidationError as e:
                raise APIWarning(str(e), codes=['mating', 'task'])
            try:
                rabbit.cleaner.check_womb()
            except ValidationError as e:
                raise APIWarning(str(e), codes=['mating', 'womb'])
    
    @staticmethod
    def _create_task(rabbit, partner):
        mother, father = (partner, rabbit) if rabbit.is_male else (rabbit, partner)
        MatingTask.objects.create(mother_rabbit=mother, father_rabbit=father)


class MotherRabbitPartnersView(_BasePartnersView):
    model = MotherRabbit
    serializer_class = MotherRabbitPartnerSerializer
    queryset = MotherRabbit.objects.all()


class FatherRabbitPartnersView(_BasePartnersView):
    model = FatherRabbit
    serializer_class = FatherRabbitPartnerSerializer
    queryset = FatherRabbit.objects.all()
