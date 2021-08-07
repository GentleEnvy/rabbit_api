from typing import Type

from api.services.model.cage.cleaners._cleaner import *

__all__ = ['CageCleanerMixin', 'FatteningCageCleanerMixin', 'MotherCageCleanerMixin']


class CageCleanerMixin:
    Cleaner: Type[CageCleaner] = CageCleaner
    
    @property
    def cleaner(self) -> CageCleaner:
        return self.Cleaner(self)
    
    def clean(self):
        # noinspection PyUnresolvedReferences
        super().clean()
        self.cleaner.clean()


class FatteningCageCleanerMixin(CageCleanerMixin):
    Cleaner = FatteningCageCleaner
    
    @property
    def cleaner(self) -> FatteningCageCleaner:
        return self.Cleaner(self)


class MotherCageCleanerMixin(CageCleanerMixin):
    Cleaner = MotherCageCleaner
    
    @property
    def cleaner(self) -> MotherCageCleaner:
        return self.Cleaner(self)
