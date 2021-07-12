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

    # INPROGRESS: branch: feature-filters-(robinson)
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        farm_number = [int(item) for item in params.get('farm_number', '-1').split(',')]
        cage_number = [int(item) for item in params.get('cage_number', '-1').split(',')]
        cage_letter = [item for item in params.get('cage_letter', [])]
        cage_type = [
            item for item in params.get('cage_type', 'fattening,mother').split(',')
        ]
        rabbits_from = int(params.get('rabbits_from', 0))
        rabbits_to = int(params.get('rabbits_to', float('inf')))
        cage_status = [item for item in params.get('cage_status', [])]
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
            **({} if len(cage_status) == 0 else {'status__in': cage_status}),
        )

        return filtered_queryset
