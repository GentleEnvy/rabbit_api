from api.models import Cage
from api.serializers import CageUpdateSerializer
from api.views.models.base import BaseDetailView

__all__ = ['CageDetailView']


class CageDetailView(BaseDetailView):
    model = Cage
    lookup_url_kwarg = 'id'
    update_serializer = CageUpdateSerializer
    queryset = Cage.objects.all()
