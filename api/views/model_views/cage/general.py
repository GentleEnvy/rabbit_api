from django.forms import model_to_dict
from rest_framework.response import Response

from api.serializers.base import BaseModelSerializer
from api.views.model_views.base import BaseGeneralView
from api.models import *
from api.views.model_views.cage._default_serializers import *

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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        farm_number = params.get('farm_number')
        cage_number = params.get('cage_number')
        letter = params.get('letter')
        cage_type = params.get('cage_type')
        rabbits_from = params.get('rabbits_from')
        rabbits_to = params.get('rabbits_to')
        cage_status = params.get('cage_status')
        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')
        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        filtered_queryset = ordered_queryset.filter(
            farm_number__in=farm_number,
            cage_number__in=cage_number,
            letter__in=letter,
            cage_type_in=cage_type,
            rabbits_in__gte=rabbits_from,
            rabbits_in__lte=rabbits_to,
            status=cage_status
        )

        if limit_from is not None:
            if limit_to is not None:
                return filtered_queryset[int(limit_from):int(limit_to)]
            return filtered_queryset[int(limit_from):]
        if limit_to is not None:
            return filtered_queryset[:int(limit_to)]
        return filtered_queryset


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
