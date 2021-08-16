from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin

from api.models import *
from api.serializers.model.task.in_progress.details.complete import *
from api.services.model.task.controllers import *
from api.services.model.task.controllers.base import TaskController
from api.views.base import BaseView
from api.views.model.base import BaseDetailView

__all__ = [
    'CompleteTaskDetailView', 'CompleteBunnyJiggingTaskDetailView',
    'CompleteSlaughterInspectionTaskDetailView'
]


class CompleteTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().waiting_completion.all()
    lookup_url_kwarg = 'id'
    update_serializer = CompleteTaskUpdateSerializer
    
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.user = None
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
