from api.models import Cage
from api.serializers import CageDetailSerializer
from api.views.model_views.base import BaseDetailView


class CageDetailView(BaseDetailView):
    model = Cage
    lookup_url_kwarg = 'id'
    update_serializer = CageDetailSerializer
    queryset = model.objects.all()
