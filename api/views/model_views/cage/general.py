from api.views.model_views.base import BaseGeneralView
from api.serializers import CageListSerializer
from api.models import Cage

__all__ = ['CageGeneralView']


class CageGeneralView(BaseGeneralView):
    model = Cage
    list_serializer = CageListSerializer
    # noinspection SpellCheckingInspection
    queryset = Cage.objects.select_related(
        'mothercage', 'fatteningcage'
    ).prefetch_related(
        'mothercage__motherrabbit_set', 'mothercage__bunny_set',
        'fatteningcage__fatteningrabbit_set', 'fatteningcage__fatherrabbit_set'
    )
