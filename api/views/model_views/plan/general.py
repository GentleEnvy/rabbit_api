from api.models import Plan
from api.serializers import PlanListSerializer
from api.views.model_views.base import BaseGeneralView

__all__ = ['PlanGeneralView']


class PlanGeneralView(BaseGeneralView):
    model = Plan
    queryset = Plan.objects.filter(is_completed=False)
    list_serializer = PlanListSerializer
