from logging import LogRecord
from typing import Optional

__all__ = ['CacheMessageLogRecord']


class CacheMessageLogRecord(LogRecord):
    # noinspection SpellCheckingInspection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__message: Optional[str] = None
    
    def getMessage(self) -> str:
        if self.__message:
            return self.__message
        return super().getMessage()
    
    def setMessage(self, message: str) -> None:
        if not self.__message:
            self.__message = message
