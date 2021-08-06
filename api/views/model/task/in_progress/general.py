from rest_framework import status
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.models import Task
from api.serializers.model.task.in_progress.general import InProgressTaskListSerializer
from api.services.model.task.controllers import all_controllers
from api.services.model.task.controllers.base import TaskController
from api.views.base import BaseView
from api.views.model.task.base import BaseTaskGeneralView

__all__ = ['InProgressTaskGeneralView', 'InProgressUpdateTaskGeneralView']


class InProgressTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = InProgressTaskListSerializer
    queryset = TaskController().in_progress.all()


# noinspection PyMethodMayBeStatic
class InProgressUpdateTaskGeneralView(BaseView):
    def post(self, request, *args, **kwargs):
        try:
            for task_controller in all_controllers:
                task_controller().update_in_progress()
        except OverflowError as e:
            # TODO: log
            raise APIWarning(str(e), codes=['overflow'])
        return Response(status=status.HTTP_202_ACCEPTED)