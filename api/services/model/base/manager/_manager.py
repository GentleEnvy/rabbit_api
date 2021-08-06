from abc import ABC
from typing import Final

__all__ = ['BaseManager']


class BaseManager(ABC):
    def __init__(self, model):
        self.model: Final = model
