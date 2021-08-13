from api.models import *
from api.serializers.model.task.in_progress.details.complete import *
from api.services.model.task.controllers import *
from api.services.model.task.controllers.base import TaskController
from api.views.model.base import BaseDetailView

__all__ = [
    'InProgressTaskDetailView', 'InProgressBunnyJiggingTaskDetailView',
    'InProgressSlaughterInspectionTaskDetailView'
]


class InProgressTaskDetailView(BaseDetailView):
    model = Task
    queryset = TaskController().in_progress.filter(
        bunnyjiggingtask=None, slaughterinspectiontask=None
    )
    lookup_url_kwarg = 'id'
    update_serializer = CompleteTaskUpdateSerializer


class InProgressBunnyJiggingTaskDetailView(InProgressTaskDetailView):
    model = BunnyJiggingTask
    queryset = BunnyJiggingTaskController().in_progress
    update_serializer = CompleteBunnyJiggingTaskUpdateSerializer


class InProgressSlaughterInspectionTaskDetailView(InProgressTaskDetailView):
    model = SlaughterInspectionTask
    queryset = SlaughterInspectionTaskController().in_progress
    update_serializer = CompleteSlaughterInspectionTaskUpdateSerializer
