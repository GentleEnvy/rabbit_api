from typing import Type

from api.services.model.cage.managers._manager import *

__all__ = [
    'CageManagerMixin', 'MotherCageManagerMixin', 'FatteningCageManagerMixin'
]


class CageManagerMixin:
    Manager: Type[CageManager] = CageManager
    
    @property
    def manager(self) -> CageManager:
        return self.Manager(self)


class MotherCageManagerMixin(CageManagerMixin):
    Manager = MotherCageManager
    
    @property
    def manager(self) -> MotherCageManager:
        return self.Manager(self)


class FatteningCageManagerMixin(CageManagerMixin):
    Manager = FatteningCageManager
    
    @property
    def manager(self) -> FatteningCageManager:
        return self.Manager(self)
