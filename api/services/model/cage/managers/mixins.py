from api.services.model.base.manager.mixin import BaseManagerMixin
from api.services.model.cage.managers._manager import *

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
