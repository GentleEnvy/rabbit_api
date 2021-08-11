from api.models import Task
from api.serializers.model.task.anonymous.detail import AnonymousTaskUpdateSerializer
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = ['AnonymousTaskDetailView']


class AnonymousTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().anonymous.all()
    lookup_url_kwarg = 'id'
    update_serializer = AnonymousTaskUpdateSerializer
