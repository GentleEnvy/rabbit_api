from api.models import Rabbit, DeadRabbit, Cage
from api.serializers import (
    RabbitListSerializer, MotherRabbitCreateSerializer,
    FatherRabbitCreateSerializer
)
from api.views.model_views.base import BaseGeneralView

__all__ = [
    'RabbitGeneralView', 'MotherRabbitGeneralView', 'FatherRabbitGeneralView'
]


class RabbitGeneralView(BaseGeneralView):
    model = Rabbit
    list_serializer = RabbitListSerializer
    # noinspection SpellCheckingInspection
    queryset = Rabbit.objects.exclude(current_type=DeadRabbit.CHAR_TYPE).select_related(
        'bunny', 'bunny__cage',
        'fatteningrabbit', 'fatteningrabbit__cage',
        'motherrabbit', 'motherrabbit__cage',
        'fatherrabbit', 'fatherrabbit__cage'
    ).all()

    # INPROGRESS: branch: feature-filters-(robinson)
    # FIXME: filters
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        farm_number = params.get('farm_number')
        gender = params.get('gender')
        rabbit_type = params.get('type')
        # breed = params.get('breed')
        status = params.get('status')
        age_from = params.get('age_from', 0)
        age_to = params.get('age_to', float('inf'))
        weight_from = params.get('weight_from', 0)
        weight_to = params.get('weight_to', float('inf'))

        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')

        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        filtered_queryset = ordered_queryset.filter(
            # не уверен, что это правильное решение для pk
            pk__in=[
                rabbit.id for rabbit in ordered_queryset
                if any(s in rabbit.cast.manager.status for s in status) and rabbit.cast.cage.farm_number in farm_number
            ] + [
                rabbit.id for rabbit in ordered_queryset
                if age_from < rabbit.cast.manager.age < age_to and weight_from < rabbit.weight < weight_to
            ],
            is_male=True if gender == 'male' else False,
            current_type=rabbit_type,

        )

        if limit_from is not None:
            if limit_to is not None:
                return filtered_queryset[int(limit_from):int(limit_to)]
            return filtered_queryset[int(limit_from):]
        if limit_to is not None:
            return filtered_queryset[:int(limit_to)]
        return filtered_queryset


class MotherRabbitGeneralView(BaseGeneralView):
    model = MotherRabbitCreateSerializer.Meta.model
    create_serializer = MotherRabbitCreateSerializer
    queryset = model.objects.all()


class FatherRabbitGeneralView(BaseGeneralView):
    model = FatherRabbitCreateSerializer.Meta.model
    create_serializer = FatherRabbitCreateSerializer
    queryset = model.objects.all()
