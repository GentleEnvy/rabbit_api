from __future__ import annotations

from typing import Final, Union, Optional, Callable, Type

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as RestFrameworkValidationError
from rest_framework.response import Response

__all__ = ['APIException', 'APIError']


def _cast_rest_framework_validation_error(exception: RestFrameworkValidationError):
    return APIException(message=str(exception.get_full_details()), status=400)


def _cast_django_validation_error(exception: DjangoValidationError):
    return APIException(message=str(exception.messages), status=400)


class APIException(Exception):
    __EXCEPTIONS__CAST: Final[dict[
        Type[Exception],
        Callable[[Exception], APIException]
    ]] = {
        RestFrameworkValidationError: _cast_rest_framework_validation_error,
        DjangoValidationError: _cast_django_validation_error
    }
    
    SUPPORT_TO_CAST_EXCEPTIONS: Final[tuple[Exception]] = tuple(__EXCEPTIONS__CAST)
    
    @classmethod
    def cast_exception(cls, exception: Exception) -> APIException:
        if caster := cls.__EXCEPTIONS__CAST.get(type(exception)):
            return caster(exception)
        raise ValueError(f'Casting is not supported for {type(exception)}')
    
    def __init__(self, status: int = 500, message: str = 'Critical server exception'):
        self.status: Final[int] = status
        self.message: Final[str] = message
    
    def to_response(self) -> Response:
        return Response(data=self.message, status=self.status)


class APIError(APIException):
    def __init__(self, status=400, message='Critical server error', code: str = None):
        super().__init__(status, message)
        self.code: Final[Optional[str]] = code
    
    def serialize(self) -> dict[str, dict[str, Union[int, str]]]:
        json = {'error': {}}
        if self.code is not None:
            json['error']['code'] = self.code
        if self.message is not None:
            json['error']['message'] = self.message
        return json
