# taken from https://gist.github.com/SehgalDivij/1ca5c647c710a2c3a0397bce5ec1c1b4

"""
Middleware to log all requests and responses.
Uses a logger configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""
import logging
import time
import json

from django.utils.deprecation import MiddlewareMixin

__all__ = ['RequestLogMiddleware']

logger = logging.getLogger('api')


# noinspection PyMethodMayBeStatic
class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware."""
    
    def __init__(self, *args, **kwargs):
        """Constructor method."""
        super().__init__(*args, **kwargs)
    
    def process_request(self, request):
        """Set Request Start Time to measure time taken to service request."""
        if request.method in ['POST', 'PUT', 'PATCH']:
            request.req_body = request.body
        request.start_time = time.time()
    
    def extract_log_info(self, request, response=None, **_):
        """Extract appropriate log info from requests/responses/exceptions."""
        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'run_time': time.time() - request.start_time,
        }
        if request.method in ['PUT', 'POST', 'PATCH']:
            log_data['request_body'] = request.req_body
        if response:
            log_data['response_body'] = getattr(response, 'content', b'')
        return log_data
    
    def process_response(self, request, response):
        """Log data using logger."""
        log_data = self.extract_log_info(request=request, response=response)
        logger.debug(msg=log_data)
        return response
