from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from api.serializers.auth.base import BaseAuthSerializer
from api.views.auth.base import BaseAuthView

__all__ = ['AuthTokenView']


class AuthTokenView(ObtainAuthToken, BaseAuthView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = BaseAuthSerializer
    
    post = BaseAuthView.post
    
    def _make_json_response(self, user):
        return {'token': Token.objects.get_or_create(user=user)[0].key}
