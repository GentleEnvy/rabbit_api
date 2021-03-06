from typing import Final

from django.http import Http404
from rest_framework import status as rest_status
from rest_framework.exceptions import (
    APIException as RestAPIException,
    AuthenticationFailed, NotFound
)

from api.exceptions.base import *
from api.logs import warning

__all__ = ['APIWarning']


def _cast_rest_api_exception(exception: RestAPIException):
    return APIWarning(
        exception.get_full_details(), getattr(exception, 'status_code'),
        *exception.get_codes()
    )


def _cast_404(exception: Http404):
    return APIWarning(str(exception), rest_status.HTTP_404_NOT_FOUND, ['not_found'])


class APIWarning(CastSupportsError):
    KEY_NAME = 'warning'
    LOG_FUNC = warning
    
    EXCEPTION__CAST = {
        AuthenticationFailed: _cast_rest_api_exception,
        Http404: _cast_404,
        NotFound: _cast_404
    }
    
    def __init__(self, message=None, status=None, codes: list[str] = None):
        super().__init__(
            message or 'Warning', status or rest_status.HTTP_200_OK
        )
        self.codes: Final[tuple[str, ...]] = tuple(codes or [])
    
    def serialize(self):
        json = super().serialize()
        if self.codes:
            json[self.KEY_NAME]['codes'] = self.codes
        return json
