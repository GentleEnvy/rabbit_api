from typing import Type

from api.services.model.base.manager._manager import BaseManager

__all__ = ['BaseManagerMixin']


class BaseManagerMixin:
    _manager: Type[BaseManager]
    
    @property
    def manager(self):
        return self._manager(self)
