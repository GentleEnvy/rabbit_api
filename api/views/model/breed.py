from api.models import Breed
from api.serializers.model.breed import BreedListSerializer
from api.views.model.base import BaseGeneralView

__all__ = ['BreedGeneralView']


class BreedGeneralView(BaseGeneralView):
    model = Breed
    list_serializer = BreedListSerializer
    queryset = Breed.objects.all()
