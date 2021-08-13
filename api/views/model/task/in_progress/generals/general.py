from api.models import Task
from api.serializers.model.task.in_progress.general import InProgressTaskListSerializer
from api.services.model.task.controllers.base import TaskController
from api.views.model.task.base import BaseTaskGeneralView

__all__ = ['InProgressTaskGeneralView']


class InProgressTaskGeneralView(BaseTaskGeneralView):
    model = Task
    list_serializer = InProgressTaskListSerializer
    queryset = TaskController().in_progress.all()
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        
        if (is_completed := params.get('is_completed')) is not None:
            is_completed = int(is_completed)
            if is_completed:
                queryset = queryset.exclude(completed_at=None)
            else:
                queryset = queryset.filter(completed_at=None)
        
        return queryset
