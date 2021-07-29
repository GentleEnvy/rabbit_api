from api.models import *
from api.serializers import AnonymousTaskListSerializer
from api.services.controllers import *
from api.services.controllers.task.base import TaskController
from api.views.model_views.base import BaseGeneralView

__all__ = ['AnonymousTaskGeneralView']


class AnonymousTaskGeneralView(BaseGeneralView):
    model = Task
    list_serializer = AnonymousTaskListSerializer
    # noinspection SpellCheckingInspection
    queryset = TaskController().anonymous.select_subclasses()
    
    def get(self, request, *args, **kwargs):
        for task_controller in all_controllers:
            task_controller().update_anonymous()
        return super().get(request, *args, **kwargs)
