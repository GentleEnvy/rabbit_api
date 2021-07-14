from django.db.models import Q

from api.views.model_views.base import BaseGeneralView
from api.serializers import CageListSerializer
from api.models import Cage, FatteningCage

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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params

        if farm_number := params.get('farm_number'):
            queryset = queryset.filter(farm_number__in=farm_number.split(','))

        if status := params.get('status'):
            status = status.split(',')
            if len(status) == 1:
                queryset = queryset.filter(status=status)
            elif len(status) == 2:
                queryset = queryset.filter(Q(status=status) | Q(status=status[::-1]))
            else:
                raise ValueError('Too many statuses')
        if type_ := params.get('type'):
            type_ = type_.split(',')
        number_rabbits_from = params.get('number_rabbits_from')
        number_rabbits_to = params.get('number_rabbits_to')

        filtered_queryset = queryset.filter(**(farm_number | status))
        filtered_queryset = filtered_queryset.filter(pk__in=[

        ])

        order_by = params.get('__order_by__')

        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        id_suitable_cages = []
        for cage in ordered_queryset:
            current_type = 'fattening' if isinstance(
                cage.cast, FatteningCage
            ) else 'mother'
            if cage is not None and \
                    current_type in cage_type and \
                    rabbits_from <= len(cage.cast.rabbits) <= rabbits_to:
                id_suitable_cages.append(cage.id)

        filtered_queryset = ordered_queryset.filter(
            id__in=id_suitable_cages,
            **({} if farm_number[0] == -1 else {'farm_number__in': farm_number}),
            **({} if cage_number[0] == -1 else {'number__in': cage_number}),
            **({} if len(cage_letter) == 0 else {'letter__in': cage_letter}),
            **({} if len(cage_status) == 0 else {'status__in': cage_status})
        )

        return filtered_queryset
