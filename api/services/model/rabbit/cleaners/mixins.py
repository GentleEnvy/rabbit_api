from typing import Final

from api.services.model.rabbit.cleaners._cleaner import *

__all__ = [
    'RabbitCleanerMixin', 'DeadRabbitCleanerMixin', 'FatteningRabbitCleanerMixin',
    'BunnyCleanerMixin', 'MotherRabbitCleanerMixin', 'FatherRabbitCleanerMixin'
]


class RabbitCleanerMixin:
    Cleaner: Type[RabbitCleaner] = RabbitCleaner
    
    @property
    def cleaner(self) -> RabbitCleaner:
        return self.Cleaner(self)
    
    def clean(self):
        # noinspection PyUnresolvedReferences
        super().clean()
        self.cleaner.clean()


class DeadRabbitCleanerMixin(RabbitCleanerMixin):
    Cleaner: Final = DeadRabbitCleaner
    
    @property
    def cleaner(self) -> DeadRabbitCleaner:
        return self.Cleaner(self)


class FatteningRabbitCleanerMixin(RabbitCleanerMixin):
    Cleaner: Final = FatteningRabbitCleaner
    
    @property
    def cleaner(self) -> FatteningRabbitCleaner:
        return self.Cleaner(self)


class BunnyCleanerMixin(RabbitCleanerMixin):
    Cleaner: Final = BunnyCleaner
    
    @property
    def cleaner(self) -> BunnyCleaner:
        return self.Cleaner(self)


class MotherRabbitCleanerMixin(RabbitCleanerMixin):
    Cleaner: Final = MotherRabbitCleaner
    
    @property
    def cleaner(self) -> MotherRabbitCleaner:
        return self.Cleaner(self)


class FatherRabbitCleanerMixin(RabbitCleanerMixin):
    Cleaner: Final = FatherRabbitCleaner
    
    @property
    def cleaner(self) -> FatherRabbitCleaner:
        return self.Cleaner(self)
