from api.models import *
from api.serializers.model.task.in_progress.details.complete import *
from api.services.model.task.controllers import *
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = [
    'CompleteTaskDetailView', 'CompleteBunnyJiggingTaskDetailView',
    'CompleteSlaughterInspectionTaskDetailView'
]


class CompleteTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().waiting_completion.filter(
        bunnyjiggingtask=None, slaughterinspectiontask=None
    )
    lookup_url_kwarg = 'id'
    update_serializer = CompleteTaskUpdateSerializer


class CompleteBunnyJiggingTaskDetailView(CompleteTaskDetailView):
    model = BunnyJiggingTask
    queryset = BunnyJiggingTaskController().in_progress
    update_serializer = CompleteBunnyJiggingTaskUpdateSerializer


class CompleteSlaughterInspectionTaskDetailView(CompleteTaskDetailView):
    model = SlaughterInspectionTask
    queryset = SlaughterInspectionTaskController().in_progress
    update_serializer = CompleteSlaughterInspectionTaskUpdateSerializer
