from api.models import Plan
from api.serializers import PlanListSerializer, PlanCreateSerializer
from api.views.model_views.base import BaseGeneralView

__all__ = ['PlanGeneralView']


class PlanGeneralView(BaseGeneralView):
    model = Plan
    queryset = Plan.objects.all()
    list_serializer = PlanListSerializer
    create_serializer = PlanCreateSerializer
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        if date := params.get('date'):
            queryset = queryset.filter(date=date)
        return queryset
