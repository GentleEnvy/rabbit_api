from rest_framework import status as rest_status
from rest_framework.exceptions import (
    ValidationError as RestValidationError, APIException as RestAPIException,
    NotAuthenticated
)

from api.exceptions.base import *

__all__ = ['ClientError']


def _cast_rest_api_exception(exception: RestAPIException):
    return ClientError(exception.get_full_details(), getattr(exception, 'status_code'))


def _cast_rest_validation_error(exception: RestValidationError):
    return ClientError(exception.get_full_details(), getattr(exception, 'status_code'))


class ClientError(CastSupportsError):
    KEY_NAME = 'client_error'
    
    EXCEPTION__CAST = {
        RestValidationError: _cast_rest_validation_error,
        NotAuthenticated: _cast_rest_api_exception
    }
    
    def __init__(self, message=None, status=None):
        super().__init__(
            message or 'Client error', status or rest_status.HTTP_400_BAD_REQUEST
        )
