from api.models import Task
from api.serializers.model.task.in_progress.general import InProgressTaskListSerializer
from api.services.model.task.controllers.base import TaskController
from api.views.model.task.base import BaseTaskGeneralView

__all__ = ['CompleteTaskGeneralView']


class CompleteTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = InProgressTaskListSerializer
    queryset = TaskController().waiting_completion.all()
