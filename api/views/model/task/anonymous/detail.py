from api.models import Task
from api.serializers.model.task.anonymous.detail import AnonymousTaskUpdateSerializer
from api.services.model.task.controllers import all_controllers
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = ['AnonymousTaskDetailView']


class AnonymousTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().anonymous.all()
    lookup_url_kwarg = 'id'
    update_serializer = AnonymousTaskUpdateSerializer
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        task = serializer.instance
        for controller_class in all_controllers:
            if isinstance(task, controller_class.task_model):
                controller_class().setup(task)
