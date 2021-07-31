from api.models import Task
from api.serializers import InProgressTaskListSerializer
from api.services.controllers import *
from api.services.controllers.task.base import TaskController
from api.views.base import BaseView
from api.views.model_views.task.base import BaseTaskGeneralView

__all__ = ['InProgressTaskGeneralView', 'InProgressUpdateTaskGeneralView']


class InProgressTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = InProgressTaskListSerializer
    queryset = TaskController().in_progress.all()


# noinspection PyMethodMayBeStatic
class InProgressUpdateTaskGeneralView(BaseView):
    def post(self, request, *args, **kwargs):
        for task_controller in all_controllers:
            task_controller().update_in_progress()
