from api.models import Plan
from api.serializers import PlanListSerializer, PlanCreateSerializer
from api.views.model_views.base import BaseGeneralView

__all__ = ['PlanGeneralView']


class PlanGeneralView(BaseGeneralView):
    model = Plan
    queryset = Plan.objects.all()
    list_serializer = PlanListSerializer
    create_serializer = PlanCreateSerializer
