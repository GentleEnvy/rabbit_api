from typing import final, Type

from api.models import *
from api.views.model.base import BaseGeneralView

__all__ = ['BaseTaskGeneralView']

_char_type__task_class = {
    task_class.CHAR_TYPE: task_class for task_class in (
        ToReproductionTask, ToFatteningTask, MatingTask, BunnyJiggingTask,
        VaccinationTask, SlaughterInspectionTask, SlaughterTask
    )
}


class BaseTaskGeneralView(BaseGeneralView):
    @final
    def filter_queryset(self, queryset):
        params = self.request.query_params
        
        queryset = super().filter_queryset(queryset)
        queryset = self._filter_queryset(queryset)
        grouped_tasks = self.__grouping(queryset)
        
        if (order := params.get('__order_by__')) is not None:
            return self.__order(grouped_tasks, order)
        return sum(map(list, grouped_tasks.values()), start=[])
    
    def _filter_queryset(self, queryset):
        params = self.request.query_params
        
        user = params.get('user')
        if user is not None:
            queryset = queryset.filter(user_id=user)
        
        return queryset
    
    @staticmethod
    def __grouping(queryset) -> dict[Type[Task], list[Task]]:
        grouped_tasks = {task_class: [] for task_class in _char_type__task_class.values()}
        for task in queryset.all():
            grouped_tasks[type(task)].append(task)
        return grouped_tasks
    
    @staticmethod
    def __order(grouped_tasks, order) -> list[Task]:
        first_tasks = grouped_tasks.pop(_char_type__task_class[order])
        return sum(map(list, grouped_tasks.values()), start=list(first_tasks))
