from http import HTTPStatus
from typing import Type

from rest_framework.response import Response

from api.models import *
from api.views.base import BaseView

__all__ = [
    'FatteningRabbitRecastView', 'MotherRabbitRecastView', 'FatherRabbitRecastView'
]


class _BaseRecastView(BaseView):
    lookup_url_kwarg = 'id'
    task_model: Type[Task]
    
    # noinspection PyMethodMayBeStatic
    def post(self, request, _):
        rabbit = self.get_object()
        self.task_model.objects.create(rabbit=rabbit)
        return Response(status=HTTPStatus.NO_CONTENT)


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
