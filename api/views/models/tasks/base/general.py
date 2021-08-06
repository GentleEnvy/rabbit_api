from api.models import *
from api.views.models.base import BaseGeneralView

__all__ = ['BaseTaskGeneralView']

_char_type__task_class = {
    task_class.CHAR_TYPE: task_class for task_class in (
        ToReproductionTask, ToFatteningTask, MatingTask, BunnyJiggingTask,
        VaccinationTask, SlaughterInspectionTask, SlaughterTask
    )
}


class BaseTaskGeneralView(BaseGeneralView):
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        
        if order := params.get('__order_by__'):
            return queryset.order_by(_char_type__task_class[order].__name__.lower())
        return queryset
