from django.utils.deprecation import MiddlewareMixin

__all__ = ['NotEmptyResponseMiddleware']


# noinspection PyMethodMayBeStatic, PyBroadException
class NotEmptyResponseMiddleware(MiddlewareMixin):
    def process_response(self, _, response):
        if getattr(response, 'content', b'') == b'':
            response.content = b'{}'
        return response
