from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

from api.utils.functions import to_datetime
from api.views.base import BaseView
from api.models.unmanaged.operations import *


class OperationView(BaseView):
    FILTER_QUERY_PARAMS = ('rabbit_id', 'time_from', 'time_to')
    ORDER_BY_TIME = 'T'

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        filters = self._get_filters(request)
        type_ = request.query_params.get('type')
        if (time_from := request.query_params.get('time_from')) is not None:
            filters['time_from'] = to_datetime(time_from)
        if (time_to := request.query_params.get('time_to')) is not None:
            filters['time_to'] = to_datetime(time_to)
        order_by = request.query_params.get('__order_by__', self.ORDER_BY_TIME)
        limit_from = request.query_params.get('__limit_from__', 0)
        limit_to = request.query_params.get('__limit_to__')

        operations = []
        for operation_class in (
                BirthOperation, SlaughterOperation, VaccinationOperation, MatingOperation,
                JiggingOperation
        ):
            if type_ is None or type_ == operation_class.CHAR_TYPE:
                operations.extend(operation_class.search(**filters))

        self._sort_operations(operations, order_by)
        operations = self._slice_operations(operations, limit_from, limit_to)
        return Response({
            'operations': [operation.serialize() for operation in operations]
        })

    def _get_filters(self, request: Request) -> dict[str, Any]:
        return {
            key: value for key, value in request.query_params.items()
            if key in self.FILTER_QUERY_PARAMS
        }

    def _sort_operations(self, operations: list, order_by: str) -> None:
        if order_by == self.ORDER_BY_TIME:
            operations.sort(key=lambda o: o.time, reverse=True)

    @staticmethod
    def _slice_operations(operations: list, from_: int, to: int = None) -> list:
        if to is None:
            return operations[from_:]
        return operations[from_:to]
