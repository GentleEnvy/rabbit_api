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
from api.services.filterers import RabbitFilterer
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
        params = self.request.query_params.copy()
        if is_male := params.get('is_male'):
            params['is_male'] = bool(int(is_male))
        if type_ := params.get('type'):
            params['type'] = tuple(type_.split(','))
        if breed := params.get('breed'):
            params['breed'] = tuple(map(int, breed.split(',')))
        if age_from := params.get('age_from'):
            params['age_from'] = datetime.utcnow() - timedelta(int(age_from))
        if age_to := params.get('age_to'):
            params['age_to'] = datetime.utcnow() - timedelta(int(age_to))
        if weight_from := params.get('weight_from'):
            params['weight_from'] = float(weight_from)
        if weight_to := params.get('weight_to'):
            params['weight_to'] = float(weight_to)
        if status := params.get('status'):
            params['status'] = tuple(status.split(','))
        if farm_number := params.get('farm_number'):
            params['farm_number'] = tuple(map(int, farm_number.split(',')))
        filterer = RabbitFilterer(queryset)
        filterer.filter(**params)
        if order_by := params.get('__order_by__'):
            return filterer.order_set(order_by)
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
