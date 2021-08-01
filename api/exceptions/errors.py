from __future__ import annotations

from typing import Final

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from api.exceptions.base import *

__all__ = ['ClientError', 'CriticalError', 'APIWarning']


class ClientError(CastSupportsError):
    key_name = 'client_error'
    
    @staticmethod
    def _cast_rest_framework_validation_error(exception: RestFrameworkValidationError):
        return ClientError(message=str(exception.get_full_details()))
    
    @staticmethod
    def _cast_django_validation_error(exception: DjangoValidationError):
        return ClientError(message=str(exception))
    
    EXCEPTION__CAST = {
        DjangoValidationError: _cast_django_validation_error,
        RestFrameworkValidationError: _cast_rest_framework_validation_error
    }
    
    def __init__(self, message='Client error'):
        super().__init__(message, 400)


class CriticalError(CastSupportsError):
    key_name = 'critical_error'
    
    @staticmethod
    def _cast_exception(exception: Exception):
        return CriticalError(str(exception))
    
    EXCEPTION__CAST = {
        Exception: _cast_exception
    }
    
    def __init__(self, message='Critical server error'):
        super().__init__(message, 500)


class APIWarning(APIException):
    key_name = 'warning'
    
    def __init__(self, message='Critical server error', status=100, code: str = None):
        super().__init__(message, status)
        self.code: Final[str] = code
    
    def serialize(self):
        json = self.serialize()
        if self.code is not None:
            json[self.key_name]['code'] = self.code
        return json
