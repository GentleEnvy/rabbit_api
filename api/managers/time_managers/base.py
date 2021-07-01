from typing import Final, Type

from datetime import datetime

from django.db.models import Model
from django.utils.timezone import now

__all__ = ['BaseTimeManager', 'BaseTimeManagerMixin']


class BaseTimeManager:
    def __init__(self, model, time: datetime = None):
        self.model: Final = model
        self.time: Final = now() if time is None else time


class BaseTimeManagerMixin(Model):
    _time_manager: Type[BaseTimeManager]

    def time_manager(self, time: datetime = None):
        return self._time_manager(self, time)
