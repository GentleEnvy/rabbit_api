from typing import Type, Optional

from rest_framework import status
from rest_framework.response import Response

from api.models import *
from api.views.base import BaseView
from api.exceptions import *

__all__ = [
    'FatteningRabbitRecastView', 'MotherRabbitRecastView', 'FatherRabbitRecastView'
]


class _BaseRecastView(BaseView):
    lookup_url_kwarg = 'id'
    task_model: Type[Task]
    
    def get(self, request, _):
        return Response({'waiting_recast': self._get_task_or_none() is not None})
    
    def post(self, request, _):
        rabbit = self.get_object()
        if self._get_task_or_none(rabbit) is not None:
            raise ClientError('The rabbit is already waiting recast')
        self.task_model.objects.create(rabbit=rabbit)
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, _):
        task = self._get_task_or_none()
        if task is None:
            raise ClientError('The rabbit does not waiting recast')
        task.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def _get_task_or_none(self, rabbit=None) -> Optional[Task]:
        if rabbit is None:
            rabbit = self.get_object()
        try:
            return self.task_model.objects.filter(
                is_confirmed=None, rabbit=rabbit
            ).latest('created_at')
        except self.task_model.DoesNotExist:
            return None


class FatteningRabbitRecastView(_BaseRecastView):
    model = FatteningRabbit
    queryset = FatteningRabbit.all_current.all()
    task_model = ToReproductionTask


class MotherRabbitRecastView(_BaseRecastView):
    model = MotherRabbit
    queryset = MotherRabbit.all_current.all()
    task_model = ToFatteningTask


class FatherRabbitRecastView(_BaseRecastView):
    model = FatherRabbit
    queryset = FatherRabbit.all_current.all()
    task_model = ToFatteningTask
