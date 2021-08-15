from rest_framework.mixins import DestroyModelMixin

from api.models import *
from api.serializers.model.task.in_progress.details.complete import *
from api.services.model.task.controllers import *
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = [
    'CompleteTaskDetailView', 'CompleteBunnyJiggingTaskDetailView',
    'CompleteSlaughterInspectionTaskDetailView'
]


class CompleteTaskDetailView(DestroyModelMixin, BaseDetailView):
    model = Task
    queryset = TaskController().waiting_completion.all()
    lookup_url_kwarg = 'id'
    update_serializer = CompleteTaskUpdateSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'GET':
            return queryset
        return queryset.filter(bunnyjiggingtask=None, slaughterinspectiontask=None)


class CompleteBunnyJiggingTaskDetailView(CompleteTaskDetailView):
    model = BunnyJiggingTask
    queryset = BunnyJiggingTaskController().in_progress
    update_serializer = CompleteBunnyJiggingTaskUpdateSerializer


class CompleteSlaughterInspectionTaskDetailView(CompleteTaskDetailView):
    model = SlaughterInspectionTask
    queryset = SlaughterInspectionTaskController().in_progress
    update_serializer = CompleteSlaughterInspectionTaskUpdateSerializer
