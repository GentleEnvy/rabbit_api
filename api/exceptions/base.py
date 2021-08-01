from __future__ import annotations

from typing import Final, Union, Type, Callable

from rest_framework.response import Response

__all__ = ['APIException', 'CastSupportsError']


class APIException(Exception):
    key_name: str
    
    def __init__(self, message: str, status: int):
        self.message: Final[str] = message
        self.status: Final[int] = status
    
    def serialize(self) -> dict[str, dict[str, str]]:
        return {self.key_name: {'message': self.message}}
    
    def to_response(self) -> Response:
        return Response(status=self.status, data=self.serialize())


class CastSupportsError(APIException):
    EXCEPTION__CAST: dict[Type[Exception], Callable[[Exception], APIException]]
    
    @classmethod
    def cast_exception(cls, exception: Exception) -> APIException:
        if caster := cls.EXCEPTION__CAST.get(type(exception)):
            return caster(exception)
        raise ValueError(f'Casting is not supported for {type(exception)}')
