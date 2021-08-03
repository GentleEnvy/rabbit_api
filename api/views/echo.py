from rest_framework.response import Response

from api.logs import critical
from api.views.base import BaseView

__all__ = ['EchoView']


# noinspection PyMethodMayBeStatic
class EchoView(BaseView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self._echo(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self._echo(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self._echo(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self._echo(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self._echo(request, *args, **kwargs)
    
    def _echo(self, request, *args, **kwargs):
        return Response(
            {
                'GET': request.GET,
                'POST': request.POST,
                'data': request.data,
                'query_params': request.query_params,
                'user': str(request.user),
                'auth': str(request.auth),
                'args': args,
                'kwargs': kwargs
            }
        )
