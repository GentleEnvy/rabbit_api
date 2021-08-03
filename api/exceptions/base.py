from __future__ import annotations

from typing import Final, Union, Type, Callable, Any

from rest_framework.response import Response

__all__ = ['APIException', 'CastSupportsError']

from api.logs import error, logger


class APIException(Exception):
    KEY_NAME: str
    
    def __init__(self, message: str, status: int):
        self.message: Final[str] = message
        self.status: Final[int] = status
    
    def serialize(self) -> dict[str, dict[str, Any]]:
        return {self.KEY_NAME: {'message': self.message}}
    
    def to_response(self) -> Response:
        return Response(data=self.serialize(), status=self.status)


class LoggedException(APIException):
    LOG_FUNC = staticmethod(error)
    
    def __init__(self, message, status, log_func=None):
        super().__init__(message, status)
        self.log_func = log_func or self.LOG_FUNC
    
    def log(self) -> None:
        self.log_func(self.message)


class CastSupportsError(LoggedException):
    EXCEPTION__CAST: dict[Type[Exception], Callable[[Exception], APIException]] = {}
    
    @classmethod
    def cast_exception(cls, exception: Exception) -> APIException:
        for exception_type, caster in cls.EXCEPTION__CAST.items():
            if issubclass(type(exception), exception_type):
                return caster(exception)
        raise ValueError(f'Casting is not supported for {type(exception)}')
