from api.models import Task
from api.serializers import AnonymousTaskUpdateSerializer
from api.services.controllers.task.base import TaskController
from api.views.model_views.base import BaseDetailView

__all__ = ['AnonymousTaskDetailView']


class AnonymousTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().anonymous.all()
    lookup_url_kwarg = 'id'
    update_serializer = AnonymousTaskUpdateSerializer
