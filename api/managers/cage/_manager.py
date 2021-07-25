from api.managers.base import *
from api import models as api_models

__all__ = [
    'CageManager', 'MotherCageManager', 'FatteningCageManager'
]


class CageManager(BaseManager):
    model: 'api_models.Cage'


class MotherCageManager(CageManager):
    model: 'api_models.MotherCage'
    
    @property
    def is_parallel(self) -> bool:
        return not self.model.has_right_womb


class FatteningCageManager(CageManager):
    model: 'api_models.FatteningCage'
