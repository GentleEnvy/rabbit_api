from rest_framework import status
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.logs import warning
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
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        user = params.get('user')
        if user is not None:
            return queryset.filter(user_id=user)
        return queryset


# noinspection PyMethodMayBeStatic
class InProgressUpdateTaskGeneralView(BaseView):
    def post(self, request, *args, **kwargs):
        for task_controller in all_controllers:
            try:
                task_controller().update_in_progress()
            except OverflowError as e:
                warning(f'Farm is full (controller: {task_controller.__name__})')
                raise APIWarning(str(e), codes=['overflow'])
        return Response(status=status.HTTP_202_ACCEPTED)
