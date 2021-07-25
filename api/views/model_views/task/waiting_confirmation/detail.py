from api.models import Task
from api.serializers import WaitingConfirmationTaskUpdateSerializer
from api.services.controllers.task.base import TaskController
from api.views.model_views.base import BaseDetailView

__all__ = ['WaitingConfirmationTaskDetailView']


class WaitingConfirmationTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().waiting_confirmation.select_subclasses()
    lookup_url_kwarg = 'id'
    update_serializer = WaitingConfirmationTaskUpdateSerializer
    
    def perform_update(self, serializer):
        # super().perform_update(serializer)
        task = serializer.instance
        # TODO: execute task
