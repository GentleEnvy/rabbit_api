from api.models import Task
from api.serializers import InProgressTaskUpdateSerializer
from api.services.controllers.task.base import TaskController
from api.views.model_views.base import BaseDetailView

__all__ = ['InProgressTaskDetailView']


class InProgressTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().in_progress.select_subclasses()
    lookup_url_kwarg = 'id'
    update_serializer = InProgressTaskUpdateSerializer
