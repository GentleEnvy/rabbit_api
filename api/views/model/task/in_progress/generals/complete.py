from threading import Thread

from rest_framework import status
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.logs import warning
from api.services.model.task.controllers import all_controllers
from api.views.base import BaseView

__all__ = ['CompleteUpdateTaskGeneralView']


def _update_all_tasks():
    for task_controller in all_controllers:
        try:
            task_controller().update_waiting_completion()
        except OverflowError as e:
            warning(f'Farm is full (controller: {task_controller.__name__})')
            raise APIWarning(str(e), codes=['overflow'])


# noinspection PyMethodMayBeStatic
class CompleteUpdateTaskGeneralView(BaseView):
    def post(self, request, *args, **kwargs):
        Thread(target=_update_all_tasks).start()
        return Response(status=status.HTTP_202_ACCEPTED)
