from api.managers.cage._manager import *
from api.managers.base import BaseManagerMixin

__all__ = [
    'CageManagerMixin', 'MotherCageManagerMixin', 'FatteningCageManagerMixin'
]


class CageManagerMixin(BaseManagerMixin):
    _manager = CageManager
    
    @property
    def manager(self) -> CageManager:
        return super().manager


class MotherCageManagerMixin(BaseManagerMixin):
    _manager = MotherCageManager
    
    @property
    def manager(self) -> MotherCageManager:
        return super().manager


class FatteningCageManagerMixin(BaseManagerMixin):
    _manager = FatteningCageManager
    
    @property
    def manager(self) -> FatteningCageManager:
        return super().manager
