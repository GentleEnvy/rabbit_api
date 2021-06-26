from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.views.exceptions import *

__all__ = ['BaseView']


class BaseView(GenericAPIView):
    def handle_exception(self, exc):
        try:
            try:
                return super().handle_exception(exc)
            except APIError as error:
                return Response(error.serialize())
            except APIException as exception:
                return exception.to_response()
            except APIException.SUPPORT_TO_CAST_EXCEPTIONS as exception_to_cast:
                return APIException.cast_exception(exception_to_cast).to_response()
        except Exception as e:
            return Response(status=400, data=str(e))
