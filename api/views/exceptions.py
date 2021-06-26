from __future__ import annotations

from typing import Final, Union, Optional, Callable, Type

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

__all__ = ['APIException', 'APIError']


def _cast_validation_error(exception: ValidationError):
    return APIException(
        status=int(exception.status_code),
        message=str(exception.detail)
    )


class APIException(Exception):
    __EXCEPTIONS__CAST: Final[dict[
        Type[Exception],
        Callable[[Exception], APIException]
    ]] = {
        ValidationError: _cast_validation_error
    }

    SUPPORT_TO_CAST_EXCEPTIONS: Final[tuple[Exception]] = tuple(__EXCEPTIONS__CAST)

    @classmethod
    def cast_exception(cls, exception: Exception) -> APIException:
        if caster := cls.__EXCEPTIONS__CAST.get(type(exception)):
            return caster(exception)
        raise ValueError(f'Casting is not supported for {type(exception)}')

    def __init__(self, status: int = 500, message: str = 'Critical server error'):
        self.status: Final[int] = status
        self.message: Final[str] = message

    def to_response(self) -> Response:
        return Response(
            status=self.status,
            data=self.message
        )


class APIError(Exception):
    def __init__(self, code: int = None, message: str = None):
        self.code: Final[Optional[int]] = code
        self.message: Final[Optional[str]] = message

    def serialize(self) -> dict[str, dict[str, Union[int, str]]]:
        json = {'error': {}}
        if self.code is not None:
            json['error']['code'] = self.code
        if self.message is not None:
            json['error']['message'] = self.message
        return json
