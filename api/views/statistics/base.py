from datetime import datetime

from rest_framework.response import Response

from api.exceptions import ClientError
from api.services.statistic import StatisticService
from api.utils.functions import to_datetime
from api.views.base import BaseView

__all__ = ['BasePeriodStatisticView', 'BaseTimeStatisticView']


class BasePeriodStatisticView(BaseView):
    def get(self, request):
        params = request.query_params
        try:
            time_from = to_datetime(params['time_from'])
        except KeyError:
            raise ClientError('Missing required parameter `time_from`')
        try:
            time_to = to_datetime(params['time_to'])
        except KeyError:
            time_to = datetime.utcnow()
        return Response(self._get(StatisticService(time_from, time_to)))
    
    def _get(self, service: StatisticService):
        raise NotImplementedError


class BaseTimeStatisticView(BaseView):
    def get(self, request):
        try:
            time = to_datetime(request.query_params['time'])
        except KeyError:
            time = datetime.utcnow()
        return Response(self._get(StatisticService(time, time)))
    
    def _get(self, service: StatisticService):
        raise NotImplementedError
