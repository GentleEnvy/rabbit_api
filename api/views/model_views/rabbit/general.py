from datetime import datetime, timedelta

from django.db.models import QuerySet
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
        'breed',
        'bunny', 'bunny__cage',
        'fatteningrabbit', 'fatteningrabbit__cage',
        'motherrabbit', 'motherrabbit__cage',
        'fatherrabbit', 'fatherrabbit__cage'
    ).prefetch_related(
        'motherrabbit__rabbit_set', 'motherrabbit__cage__bunny_set',
        'fatherrabbit__rabbit_set'
    ).all()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        if is_male := params.get('is_male', {}):
            is_male = {'is_male': bool(int(is_male))}
        if type_ := params.get('type', {}):
            type_ = {'current_type__in': type_.split(',')}
        if breed := params.get('breed', {}):
            breed = {'breed__in': list(map(int, breed.split(',')))}
        if age_from := params.get('age_from', {}):
            age_from = {'birthday__lte': datetime.utcnow() - timedelta(int(age_from))}
        if age_to := params.get('age_to', {}):
            age_to = {'birthday__gte': datetime.utcnow() - timedelta(int(age_to))}
        if weight_from := params.get('weight_from', {}):
            weight_from = {'weight__gte': weight_from}
        if weight_to := params.get('weight_to', {}):
            weight_to = {'weight__lte': weight_to}

        if status := params.get('status'):
            status = status.split(',')
        if farm_number := params.get('farm_number'):
            farm_number = list(map(int, farm_number.split(',')))

        filtered_queryset = queryset.filter(
            **(is_male | type_ | breed | age_from | age_to | weight_from | weight_to)
        )
        filtered_queryset = filtered_queryset.filter(
            id__in=[
                rabbit.id for rabbit in queryset
                if
                (
                    status is None or
                    any(s in rabbit.cast.manager.status for s in status)
                ) and (
                    farm_number is None or
                    rabbit.cast.cage.farm_number in farm_number
                )
            ]
        )

        if order_by := params.get('__order_by__'):
            return self._order_queryset(filtered_queryset, order_by)
        return filtered_queryset

    @staticmethod
    def _order_queryset(queryset: QuerySet, order_by: str):
        if order_by == 'age':
            return queryset.order_by('birthday')
        if order_by == '-age':
            return queryset.order_by('-birthday')
        if order_by == 'sex':
            return list(queryset.exclude(is_male=None).order_by('-is_male')) + \
                   list(queryset.filter(is_male=None))
        if order_by == 'farm_number':
            return sorted(queryset, key=lambda r: r.cast.cage.farm_number)
        if order_by == 'cage_number':
            return sorted(
                queryset, key=lambda r: [r.cast.cage.number, r.cast.cage.letter]
            )
        if order_by == 'type':
            return sum(
                (
                    list(queryset.filter(current_type=rabbit_class.CHAR_TYPE).all())
                    for rabbit_class in
                    (FatteningRabbit, MotherRabbit, FatherRabbit, Bunny)
                ),
                start=[]
            )
        if order_by == 'breed':
            return queryset.order_by('breed__title')
        if order_by == 'status':
            return sorted(
                queryset,
                key=lambda r: '' if len(status := r.cast.manager.status) == 0 else next(
                    iter(status)
                ), reverse=True
            )
        if order_by in ('weight', '-weight'):
            return queryset.order_by(order_by)
        return queryset


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
