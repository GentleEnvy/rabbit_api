from django.contrib.auth import login
from rest_framework.response import Response

from api.views.base import BaseView
from api.serializers import AuthSessionSerializer

__all__ = ['AuthSessionView']


class AuthSessionView(BaseView):
    serializer_class = AuthSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'username': user.username})
