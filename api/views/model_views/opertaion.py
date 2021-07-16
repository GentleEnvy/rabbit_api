from api.utils.functions import to_datetime
from api.views.model_views.base import BaseGeneralView
from api.serializers import OperationListSerializer
from api.models.unmanaged.operations import *

__all__ = ['OperationGeneralView']


class OperationGeneralView(BaseGeneralView):
    list_serializer = OperationListSerializer

    __char_type__title = {
        BirthOperation.CHAR_TYPE: 'рождение',
        SlaughterOperation.CHAR_TYPE: 'убой',
        VaccinationOperation.CHAR_TYPE: 'вакцинация',
        MatingOperation.CHAR_TYPE: 'спаривание',
        JiggingOperation.CHAR_TYPE: 'отсадка'
    }

    def get_queryset(self):
        params = self.request.query_params

        filters = {}
        if time_from := params.get('time_from'):
            filters['time_from'] = to_datetime(time_from)
        if time_to := params.get('time_to'):
            filters['time_to'] = to_datetime(time_to)

        if type_ := params.get('type'):
            type_ = type_.split(',')

        operations = []
        for operation_class in (
            BirthOperation, SlaughterOperation, VaccinationOperation, MatingOperation,
            JiggingOperation
        ):
            if type_ is None or operation_class.CHAR_TYPE in type_:
                operations.extend(operation_class.search(**filters))

        if order_by := params.get('__order_by__'):
            return self._order_queryset(operations, order_by)
        return operations

    def _order_queryset(self, operations: list, order_by: str):
        if order_by == 'time':
            operations.sort(key=lambda o: o.time, reverse=True)
        if order_by == '-time':
            operations.sort(key=lambda o: o.time, reverse=False)
        if order_by == 'type':
            operations.sort(key=lambda o: self.__char_type__title[o.CHAR_TYPE])
        return operations
