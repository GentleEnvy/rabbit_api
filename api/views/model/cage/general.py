from django.db.models import Q, QuerySet

from api.exceptions import ClientError
from api.serializers.model.cage.general import CageListSerializer
from api.views.model.base import BaseGeneralView
from api.models import *

__all__ = ['CageGeneralView']


class CageGeneralView(BaseGeneralView):
    model = Cage
    list_serializer = CageListSerializer
    # noinspection SpellCheckingInspection
    queryset = Cage.Manager.prefetch_number_rabbits().select_related(
        'mothercage__womb'
    ).order_by('id')
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        
        if farm_number := params.get('farm_number'):
            queryset = queryset.filter(farm_number__in=farm_number.split(','))
        if is_parallel := params.get('is_parallel'):
            is_parallel = bool(int(is_parallel))
        if status := params.get('status'):
            status = status.split(',')
            if len(status) == 1:
                queryset = queryset.filter(status=status)
            elif len(status) == 2:
                queryset = queryset.filter(Q(status=status) | Q(status=status[::-1]))
            else:
                raise ClientError('Too many statuses')
        elif status == '':
            queryset = queryset.filter(status=[])
        
        if type_ := params.get('type'):
            type_ = type_.split(',')
        if number_rabbits_from := params.get('number_rabbits_from'):
            number_rabbits_from = int(number_rabbits_from)
        if number_rabbits_to := params.get('number_rabbits_to'):
            number_rabbits_to = int(number_rabbits_to)
        
        queryset = queryset.filter(
            id__in=[
                cage.id for cage in queryset
                if (
                    (
                        number_rabbits_from is None or
                        number_rabbits_from <= cage.manager.number_rabbits
                    ) and (
                        number_rabbits_to is None or
                        number_rabbits_to >= cage.manager.number_rabbits
                    ) and (
                        type_ is None or cage.CHAR_TYPE in type_
                    ) and (
                        is_parallel is None or
                        isinstance(cage, FatteningCage) or (
                            cage.womb is None
                        ) == is_parallel
                    )
                )
            ]
        )
        
        if order_by := params.get('__order_by__'):
            return self._order_queryset(queryset, order_by)
        return queryset
    
    @staticmethod
    def _order_queryset(queryset: QuerySet, order_by: str):
        if order_by in ('farm_number', '-farm_number'):
            return queryset.order_by(order_by)
        if order_by == 'number':
            return queryset.order_by('number', 'letter')
        if order_by == '-number':
            return queryset.order_by('-number', '-letter')
        if order_by == 'number_rabbits':
            return sorted(queryset, key=lambda c: c.manager.number_rabbits)
        if order_by == '-number_rabbits':
            return sorted(queryset, key=lambda c: c.manager.number_rabbits, reverse=True)
        if order_by == 'status':
            return sorted(queryset, key=lambda c: [-len(c.status), c.status])
        if order_by == '-status':
            return sorted(
                queryset, key=lambda c: [-len(c.status), c.status], reverse=True
            )
        return queryset
