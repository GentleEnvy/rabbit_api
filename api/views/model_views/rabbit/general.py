from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import *
from api.serializers import (
    RabbitListSerializer, MotherRabbitCreateSerializer,
    FatherRabbitCreateSerializer
)
from api.views.model_views.base import BaseGeneralView

__all__ = ['RabbitGeneralView', 'ReproductionRabbitGeneralView']


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
        farm_number = [int(item) for item in params.get('farm_number', '-1').split(',')]
        is_male = [bool(int(item)) for item in params.get('is_male', [])]
        rabbit_type = [item for item in params.get('rabbit_type', [])]
        # breed = params.get('breed')
        status = [item for item in params.get('status', [])]
        age_from = float(params.get('age_from', 0))
        age_to = float(params.get('age_to', float('inf')))
        weight_from = float(params.get('weight_from', 0))
        weight_to = float(params.get('weight_to', float('inf')))

        order_by = params.get('__order_by__')

        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        filtered_queryset = ordered_queryset.filter(
            pk__in=[
                rabbit.id for rabbit in ordered_queryset
                if
                (len(status) == 0 or any(s in rabbit.cast.manager.status for s in status))
                and (farm_number[0] == -1 or rabbit.cast.cage.farm_number in farm_number)
                and (rabbit.weight is None or weight_from <= rabbit.weight <= weight_to)
                and age_from <= rabbit.cast.manager.age.days <= age_to
            ],
            **({} if len(rabbit_type) == 0 else {'current_type__in': rabbit_type}),
            **({} if len(is_male) == 0 else {'is_male__in': is_male}),
        )

        return filtered_queryset


class ReproductionRabbitGeneralView(BaseGeneralView):
    class __ReproductionRabbitCreateSerializer(MotherRabbitCreateSerializer):
        is_male = serializers.BooleanField(required=True)
        cage = serializers.PrimaryKeyRelatedField(queryset=Cage.objects.all())

    create_serializer = __ReproductionRabbitCreateSerializer

    def _get_male(self):
        if (is_male := self.request.data.get('is_male')) is None:
            raise ValidationError(
                {'is_male': 'The sex of the reproduction rabbit must be determined'}
            )
        return is_male

    def get_queryset(self):
        try:
            if self._get_male():
                return FatherRabbit.objects.all()
            return MotherRabbit.objects.all()
        except ValidationError:
            if settings.DEBUG:
                return Rabbit.objects.none()
            raise

    def get_serializer_class(self):
        try:
            if self._get_male():
                return FatherRabbitCreateSerializer
            return MotherRabbitCreateSerializer
        except ValidationError:
            if settings.DEBUG:
                return super().get_serializer_class()
            raise
