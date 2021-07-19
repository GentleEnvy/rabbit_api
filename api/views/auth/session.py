from api.views.auth.base import BaseAuthView
from api.serializers import AuthSessionSerializer

__all__ = ['AuthSessionView']


class AuthSessionView(BaseAuthView):
    serializer_class = AuthSessionSerializer
