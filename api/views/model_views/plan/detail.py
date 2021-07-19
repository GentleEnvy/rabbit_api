from api.models import Plan
from api.serializers.plan.detail import PlanUpdateSerializer
from api.views.model_views.base import BaseDetailView

__all__ = ['PlanDetailView']


class PlanDetailView(BaseDetailView):
    model = Plan
    lookup_url_kwarg = 'id'
    update_serializer = PlanUpdateSerializer
    queryset = Plan.objects.all()
