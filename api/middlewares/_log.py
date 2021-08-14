# taken from https://gist.github.com/SehgalDivij/1ca5c647c710a2c3a0397bce5ec1c1b4

"""
Middleware to log all requests and responses.
Uses a logger_config configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""
import json
import time

from django.utils.deprecation import MiddlewareMixin

from api.logs import debug, info

__all__ = ['RequestLogMiddleware']


def _get_content_type(request_or_response):
    return getattr(request_or_response, 'content_type', None) or getattr(
        request_or_response, 'headers', {}
    ).get('Content-Type', '')


# noinspection PyMethodMayBeStatic, PyBroadException
class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""
    
    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""
        if request.method in ['POST', 'PUT', 'PATCH']:
            request.req_body = request.body
        request.start_time = time.time()
    
    def extract_log_info(self, request, response=None, **_):
        """Extract appropriate log info from requests/responses/exceptions."""
        log_data = {
            'run_time': time.time() - request.start_time
        }
        if request.method in ['PUT', 'POST', 'PATCH']:
            content_type = _get_content_type(response)
            if 'application/json' in content_type:
                try:
                    log_data['request'] = json.dumps(
                        json.loads(request.req_body), ensure_ascii=False,
                        default=lambda o: str(o)
                    )
                except Exception:
                    log_data['request'] = request.req_body
            else:
                log_data['request'] = request.req_body
        if response:
            content_type = _get_content_type(response)
            if 'text/html' in content_type and len(response.content) > 100:
                log_data['response'] = '<<<HTML>>>'
            elif 'application/json' in content_type:
                try:
                    log_data['response'] = json.dumps(
                        response.data, ensure_ascii=False, default=lambda o: str(o)
                    )
                except Exception:
                    log_data['response'] = getattr(response, 'content', b'')
            else:
                log_data['response'] = getattr(response, 'content', b'')
        return log_data
    
    def process_response(self, request, response):
        """Log data using logger_config."""
        log_data = self.extract_log_info(request=request, response=response)
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            info(log_data)
        else:
            debug(log_data)
        return response
