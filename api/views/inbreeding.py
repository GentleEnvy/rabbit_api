from django.core.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Rabbit
from api.serializers.inbreeding import InbreedingDataSerializer
from api.services.inbreeding import AvoidInbreedingService
from api.views.base import BaseView

__all__ = ['InbreedingView']


class InbreedingView(BaseView):
    serializer_class = InbreedingDataSerializer
    
    def post(self, request):
        serializer: InbreedingDataSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rabbit_ids = serializer.validated_data['rabbits']
        rabbits = Rabbit.objects.filter(id__in=rabbit_ids)
        optimal_partners = {
            rabbit.id: self._find_optimal_partners(rabbit) for rabbit in rabbits
        }
        return Response(optimal_partners)
    
    @staticmethod
    def _find_optimal_partners(rabbit: Rabbit) -> dict[str, int]:
        avoid_inbreeding_service = AvoidInbreedingService()
        try:
            optimal_partners = avoid_inbreeding_service.find_optimal_partners(rabbit)
        except ValueError as e:
            raise ValidationError(str(e))
        return {
            partner: kinship if kinship != float('inf') else None
            for partner, kinship in optimal_partners.items()
        }
