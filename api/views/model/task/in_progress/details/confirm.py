from api.models import Task
from api.serializers.model.task.in_progress.details.confirm import *
from api.services.model.task.controllers import all_controllers
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = ['ConfirmTaskDetailView']

_task__controller = {controller.task_model: controller for controller in all_controllers}


class ConfirmTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().waiting_confirmation.all()
    lookup_url_kwarg = 'id'
    update_serializer = ConfirmTaskUpdateSerializer
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        task = serializer.instance
        controller = _task__controller[type(task)]
        if task.is_confirmed:
            controller().execute(task)
