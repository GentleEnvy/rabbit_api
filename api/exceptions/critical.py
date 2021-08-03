from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status as rest_status
from rest_framework.exceptions import APIException as RestAPIException

from api.exceptions.base import *

__all__ = ['CriticalError']


def _cast_rest_api_exception(exception: RestAPIException):
    return CriticalError(exception.get_full_details(), getattr(exception, 'status_code'))


def _cast_django_validation_error(exception: DjangoValidationError):
    if (message := getattr(exception, 'error_dict', None)) is None:
        if (message := getattr(exception, 'error_list', None)) is None:
            message = exception.message
    return CriticalError(message)


def _cast_exception(exception: Exception):
    return CriticalError(str(exception))


class CriticalError(CastSupportsError):
    KEY_NAME = 'critical_error'
    
    EXCEPTION__CAST = {
        RestAPIException: _cast_rest_api_exception,
        DjangoValidationError: _cast_django_validation_error,
        Exception: _cast_exception
    }
    
    def __init__(self, message=None, status=None):
        super().__init__(
            message or 'Critical server error',
            status or rest_status.HTTP_500_INTERNAL_SERVER_ERROR
        )
