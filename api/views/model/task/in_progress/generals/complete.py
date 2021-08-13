from threading import Thread

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from api.exceptions import APIWarning
from api.logs import warning, debug
from api.serializers.base import EmptySerializer
from api.services.model.task.controllers import all_controllers
from api.views.base import BaseView

__all__ = ['CompleteUpdateTaskGeneralView']


def _update_all_tasks():
    debug('<< start updating waiting completion tasks')
    for task_controller in all_controllers:
        try:
            task_controller().update_waiting_completion()
        except OverflowError as e:
            warning(f'Farm is full (controller: {task_controller.__name__}): {e}')
            raise APIWarning(str(e), codes=['overflow'])
    debug('waiting completion tasks update completed >>')


# noinspection PyMethodMayBeStatic
class CompleteUpdateTaskGeneralView(BaseView):
    serializer_class = EmptySerializer
    
    def get(self, request, *args, **kwargs):
        if settings.DEBUG:
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise self.http_method_not_allowed(request)
    
    def post(self, request, *args, **kwargs):
        Thread(target=_update_all_tasks).start()
        return Response(status=status.HTTP_202_ACCEPTED)
