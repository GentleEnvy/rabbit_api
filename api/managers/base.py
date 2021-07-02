from abc import ABC
from typing import Final, Type
from datetime import datetime

from django.utils.timezone import now

__all__ = ['BaseTimeManager', 'BaseTimeManagerMixin']


class BaseTimeManager(ABC):
    def __init__(self, model, time: datetime = None):
        self.model: Final = model
        self.time: Final = now() if time is None else time


class BaseTimeManagerMixin:
    _time_manager: Type[BaseTimeManager]

    def time_manager(self, time: datetime = None):
        return self._time_manager(self, time)
