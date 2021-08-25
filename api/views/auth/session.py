from api.serializers.auth.base import BaseAuthSerializer
from api.views.auth.base import BaseAuthView

__all__ = ['AuthSessionView']


class AuthSessionView(BaseAuthView):
    serializer_class = BaseAuthSerializer
