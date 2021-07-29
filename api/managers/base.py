from abc import ABC
from typing import Final, Type

__all__ = ['BaseManager', 'BaseManagerMixin']


class BaseManager(ABC):
    def __init__(self, model):
        self.model: Final = model


class BaseManagerMixin:
    _manager: Type[BaseManager]
    
    @property
    def manager(self):
        return self._manager(self)
