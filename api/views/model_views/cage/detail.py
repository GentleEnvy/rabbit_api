from api.models import *
from api.views.base import BaseView
from api.views.model_views._utils import redirect_by_id
from api.views.model_views.base import BaseDetailView
from api.views.model_views.cage._default_serializers import *

__all__ = ['CageDetailView', 'MotherCageDetailView', 'FatteningCageDetailView']


class CageDetailView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        return redirect_by_id(Cage, request, kwargs.get('id'))


class MotherCageDetailView(BaseDetailView):
    model = MotherCage
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model)
    update_serializer = create_default_update_serializer(model)
    queryset = model.objects.all()


class FatteningCageDetailView(BaseDetailView):
    model = FatteningCage
    lookup_url_kwarg = 'id'
    retrieve_serializer = create_default_retrieve_serializer(model)
    update_serializer = create_default_update_serializer(model)
    queryset = model.objects.all()
