from api.models import Task
from api.serializers import WaitingConfirmationTaskUpdateSerializer
from api.services.task.controllers import TaskController
from api.services.task.controllers import all_controllers
from api.views.model_views.base import BaseDetailView

__all__ = ['WaitingConfirmationTaskDetailView']

_task__controller = {controller.task_model: controller for controller in all_controllers}


class WaitingConfirmationTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().waiting_confirmation.all()
    lookup_url_kwarg = 'id'
    update_serializer = WaitingConfirmationTaskUpdateSerializer
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        task = serializer.instance
        controller = _task__controller[type(task)]
        controller().execute(task)
