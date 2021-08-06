from api.serializers.auth.session import AuthSessionSerializer
from api.views.auth.base import BaseAuthView

__all__ = ['AuthSessionView']


class AuthSessionView(BaseAuthView):
    serializer_class = AuthSessionSerializer
