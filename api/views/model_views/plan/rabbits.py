from api.managers import FatteningRabbitManager
from api.models import FatteningRabbit, Plan
from api.serializers import RabbitListSerializer
from api.services.filterers import RabbitFilterer
from api.views.model_views.base import BaseGeneralView

__all__ = ['PlanRabbitsView']


class PlanRabbitsView(BaseGeneralView):
    model = FatteningRabbit
    list_serializer = RabbitListSerializer
    queryset = FatteningRabbit.objects.filter(
        current_type=FatteningRabbit.CHAR_TYPE
    ).select_related('breed', 'cage').all()
    
    # TODO: query_params parser
    def filter_queryset(self, queryset):
        queryset = FatteningRabbit.objects.filter(
            current_type=FatteningRabbit.CHAR_TYPE
        ).select_related('breed', 'cage').all()
        
        params = self.request.query_params
        filters = {}
        if is_male := params.get('is_male'):
            filters['is_male'] = bool(int(is_male))
        if breed := params.get('breed'):
            filters['breed'] = list(map(int, breed.split(',')))
        if age_from := params.get('age_from'):
            filters['age_from'] = int(age_from)
        if age_to := params.get('age_to'):
            filters['age_to'] = int(age_to)
        if weight_from := params.get('weight_from'):
            filters['weight_from'] = float(weight_from)
        if weight_to := params.get('weight_to'):
            filters['weight_to'] = float(weight_to)
        if farm_number := params.get('farm_number'):
            filters['farm_number'] = list(map(int, farm_number.split(',')))
        filterer = RabbitFilterer(queryset)
        filterer.filter(
            type_=[FatteningRabbit.CHAR_TYPE],
            status=[FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER],
            **filters
        )
        return filterer.order_by_plan(Plan.objects.get(id=self.kwargs['id']))
