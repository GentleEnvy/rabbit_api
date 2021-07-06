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
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        farm_number = params.get('farm_number')
        gender = params.get('gender')
        rabbit_type = params.get('type')
        # breed = params.get('breed')
        age_from = params.get('age_from')
        age_to = params.get('age_to')
        status = params.get('status')
        weight_from = params.get('weight_from')
        weight_to = params.get('weight_to')

        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')

        filtered_queryset = queryset.filter(
            is_male=True if gender == 'male' else False,
            current_type=rabbit_type[:1].upper(),
        )

        id_suitable_farm = []
        for cage in Cage.objects.all().filter(farm_number__in=farm_number):
            rabbits = cage.cast.rabbits
            id_suitable_farm += [rabbit.id for rabbit in rabbits]

        if len(id_suitable_farm) > 0:
            filtered_queryset.filter(pk__in=id_suitable_farm)

        id_suitable_age = []
        if age_from is not None and age_to is not None:
            for rabbit in filtered_queryset:
                if age_from < rabbit.cast.manager.age < age_to:
                    id_suitable_age.append(rabbit.id)
        elif age_from is not None and age_to is None:
            for rabbit in filtered_queryset:
                if age_from < rabbit.cast.manager.age:
                    id_suitable_age.append(rabbit.id)
        elif age_from is None and age_to is not None:
            for rabbit in filtered_queryset:
                if rabbit.cast.manager.age < age_to:
                    id_suitable_age.append(rabbit.id)
        if len(id_suitable_age) > 0:
            filtered_queryset = filtered_queryset.filter(pk__in=id_suitable_age)

        id_suitable_weight = []
        if weight_from is not None and weight_to is not None:
            for rabbit in filtered_queryset:
                if weight_from < rabbit.weight < weight_to:
                    id_suitable_weight.append(rabbit.id)
        elif weight_from is not None and weight_to is None:
            for rabbit in filtered_queryset:
                if weight_from < rabbit.weight:
                    id_suitable_weight.append(rabbit.id)
        elif weight_from is None and weight_to is not None:
            for rabbit in filtered_queryset:
                if rabbit.weight < weight_to:
                    id_suitable_weight.append(rabbit.id)
        if len(id_suitable_weight) > 0:
            filtered_queryset = filtered_queryset.filter(pk__in=id_suitable_weight)

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
