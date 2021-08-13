from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

__all__ = ['NotEmptyResponseMiddleware']


# noinspection PyMethodMayBeStatic
class NotEmptyResponseMiddleware(MiddlewareMixin):
    def process_response(self, _, response):
        if getattr(response, 'content', b'') == b'':
            response.content = b'{}'
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response.status_code = status.HTTP_200_OK
        return response
