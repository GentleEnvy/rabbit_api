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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        # выбирается только 1 ферма, ограничений на выбор клеток и букв нет
        farm_number = params.get('farm_number')
        cage_number = params.get('cage_number', [i for i in range(1, len(Cage.objects.filter(farm_number=farm_number)))])
        letter = params.get('letter', ['а', 'б', 'в', 'г'])
        cage_type = params.get('cage_type')
        rabbits_from = params.get('rabbits_from', 0)
        rabbits_to = params.get('rabbits_to', float('inf'))
        cage_status = params.get('cage_status', ['C', 'R', ''])
        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')
        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        id_suitable_cages = []
        for cage in ordered_queryset:
            if cage.farm_number in farm_number \
                    and cage.number in cage_number \
                    and cage.letter in letter \
                    and cage.cast.type == cage_type \
                    and rabbits_from <= len(cage.cast.rabbits) <= rabbits_to:
                id_suitable_cages.append(cage.id)

        filtered_queryset = ordered_queryset.filter(
            id__in=id_suitable_cages,
            status__in=cage_status
        )

        if limit_from is not None:
            if limit_to is not None:
                return filtered_queryset[int(limit_from):int(limit_to)]
            return filtered_queryset[int(limit_from):]
        if limit_to is not None:
            return filtered_queryset[:int(limit_to)]
        return filtered_queryset
