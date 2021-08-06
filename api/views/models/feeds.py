from datetime import datetime
from typing import Type

from django.db.models import Sum, Q
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from api.models import *
from api.serializers.model.feed import *
from api.services.model.feed import FeedingService
from api.services.model.feed import *
from api.views.models.base import BaseGeneralView

__all__ = ['FatteningFeedsView', 'MotherFeedsView']


class _BaseFeedsView(BaseGeneralView):
    model: Type[Feeds]
    _feeding_service_class: Type[FeedingService]
    
    def get(self, request, **_):
        aggregator = self.model.objects.aggregate(
            stocks__sum=Sum('stocks', filter=Q(time__lte=datetime.utcnow()))
        )
        feeding_service = self._feeding_service_class()
        return Response(
            {
                'all_stocks': aggregator['stocks__sum'] or 0,
                'expected_stock': feeding_service.get_expected_stock(),
                'predict_bags': feeding_service.predict_bags_need_in_future()
            }
        )


class FatteningFeedsView(_BaseFeedsView):
    model = FatteningFeeds
    create_serializer = FatteningFeedsCreateSerializer
    _feeding_service_class = FatteningFeedingService


class MotherFeedsView(_BaseFeedsView):
    model = MotherFeeds
    create_serializer = MotherFeedsCreateSerializer
    _feeding_service_class = MotherFeedingService
