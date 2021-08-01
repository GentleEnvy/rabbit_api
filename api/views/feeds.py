from datetime import datetime

from django.db.models import Sum, Q
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from api.models import *
from api.serializers.feeds import *
from api.views.base import BaseView

__all__ = ['FatteningFeedsView', 'MotherFeedsView']


class _BaseFeedsView(CreateModelMixin, BaseView):
    def get(self, request):
        all_feeds = self.get_queryset()
        return Response({'all_feeds': all_feeds})


class FatteningFeedsView(_BaseFeedsView):
    queryset = FatteningFeeds.objects.aggregate(
        stocks__sum=Sum('stocks', filter=Q(time__lte=datetime.utcnow()))
    )
    serializer_class = FatteningFeedsCreateSerializer


class MotherFeedsView(_BaseFeedsView):
    queryset = MotherFeeds.objects.aggregate(
        stocks__sum=Sum('stocks', filter=Q(time__lte=datetime.utcnow()))
    )
    serializer_class = MotherFeedsCreateSerializer
