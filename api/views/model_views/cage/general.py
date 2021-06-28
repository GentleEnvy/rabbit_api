from django.forms import model_to_dict
from rest_framework.response import Response

from api.serializers.base import BaseModelSerializer
from api.views.model_views.base import BaseGeneralView
from api.models import *
from api.views.model_views.cage._default_serializers import \
    create_default_retrieve_serializer

__all__ = ['CageGeneralView', 'MotherCageGeneralView', 'FatteningCageGeneralView']


class CageGeneralView(BaseGeneralView):
    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = Cage
            fields = ['id']

    model = Cage
    list_serializer = __ListSerializer
    queryset = Cage.objects.all().values('id')

    def list(self, request, *args, **kwargs):
        super_list = super().list(request, *args, **kwargs)
        ids = [cage_info['id'] for cage_info in super_list.data]
        mother_cages = MotherCage.objects.filter(id__in=ids)
        fattening_cages = FatteningCage.objects.filter(id__in=ids)
        cage_list = []
        for cages, type_cage in zip(
                (mother_cages, fattening_cages),
                ('mother_cage', 'fattening_cage')
        ):
            for cage in cages:
                cage_info = model_to_dict(cage) | {'_type_': type_cage}
                cage_info.pop('cage_ptr')
                cage_list.append(cage_info)
        return Response(cage_list)


class MotherCageGeneralView(BaseGeneralView):
    model = MotherCage
    list_serializer = create_default_retrieve_serializer(model)
    create_serializer = create_default_retrieve_serializer(model)
    queryset = model.objects.all()


class FatteningCageGeneralView(BaseGeneralView):
    model = FatteningCage
    list_serializer = create_default_retrieve_serializer(model)
    create_serializer = create_default_retrieve_serializer(model)
    queryset = model.objects.all()
