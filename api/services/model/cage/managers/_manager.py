from api.services.model.base.manager._manager import *
from api import models as api_models

__all__ = [
    'CageManager', 'MotherCageManager', 'FatteningCageManager'
]


class CageManager(BaseManager):
    model: 'models.Cage'


class MotherCageManager(CageManager):
    model: 'models.MotherCage'
    
    @property
    def is_parallel(self) -> bool:
        return not self.model.has_right_womb


class FatteningCageManager(CageManager):
    model: 'models.FatteningCage'
