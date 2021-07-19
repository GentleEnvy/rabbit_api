from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from api.views.auth.base import BaseAuthView

__all__ = ['AuthTokenView']


class AuthTokenView(ObtainAuthToken, BaseAuthView):
    post = BaseAuthView.post
    
    def _make_json_response(self, user) -> dict:
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key}
