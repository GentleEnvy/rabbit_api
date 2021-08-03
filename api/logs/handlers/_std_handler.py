import logging
from logging import StreamHandler
from sys import stdout, stderr
from typing import Final

from api.logs.handlers.base import BaseHandler

__all__ = ['StdHandler']


class StdHandler(BaseHandler, StreamHandler):
    def __init__(self, err_level: int = logging.WARNING, *args, **kwargs):
        StreamHandler.__init__(self, stdout)
        BaseHandler.__init__(self, *args, **kwargs)
        self._err_level: Final[int] = err_level
    
    def emit(self, record):
        if record.exc_info or record.levelno >= self._err_level:
            self.stream = stderr
        StreamHandler.emit(self, record)
        self.stream = stdout
