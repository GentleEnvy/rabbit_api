from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.views.base import BaseView

__all__ = ['EchoView']


# noinspection PyMethodMayBeStatic
class EchoView(BaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'GET': request.GET,
                'POST': request.POST,
                'data': request.data,
                'user': str(request.user),
                'auth': str(request.auth),
                'args': args,
                'kwargs': kwargs
            }
        )
