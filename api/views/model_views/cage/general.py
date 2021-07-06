from api.views.model_views.base import BaseGeneralView
from api.serializers import CageGeneralSerializer
from api.models import Cage

__all__ = ['CageGeneralView']


class CageGeneralView(BaseGeneralView):
    model = Cage
    list_serializer = CageGeneralSerializer
    queryset = Cage.objects.select_related(
        'mothercage', 'fatteningcage'
    ).prefetch_related(
        'mothercage__motherrabbit_set',
        'fatteningcage__fatteningrabbit_set', 'fatteningcage__fatherrabbit_set'
    )
