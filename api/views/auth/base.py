from django.contrib.auth import login
from django.db.models import F
from rest_framework.response import Response

from api.views.base import BaseView

__all__ = ['BaseAuthView']


class BaseAuthView(BaseView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(
            {'user': self.serialize_user(user)} | self._make_json_response(user)
        )
    
    @staticmethod
    def serialize_user(user):
        # noinspection SpellCheckingInspection
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'groups': [g['type'] for g in user.groups.values(type=F('typegroup__type'))]
        }
    
    def _make_json_response(self, user) -> dict:
        return {}
