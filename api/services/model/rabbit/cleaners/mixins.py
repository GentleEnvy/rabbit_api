from typing import Type

from api.services.model.rabbit.cleaners._cleaner import *

__all__ = [
    'RabbitCleanerMixin', 'DeadRabbitCleanerMixin', 'FatteningRabbitCleanerMixin',
    'BunnyCleanerMixin', 'MotherRabbitCleanerMixin', 'FatherRabbitCleanerMixin'
]


class RabbitCleanerMixin:
    _cleaner: Type[RabbitCleaner] = RabbitCleaner
    
    @property
    def cleaner(self) -> RabbitCleaner:
        return self._cleaner(self)
    
    def clean(self):
        # noinspection PyUnresolvedReferences
        super().clean()
        self.cleaner.clean()


class DeadRabbitCleanerMixin(RabbitCleanerMixin):
    _cleaner = DeadRabbitCleaner

    @property
    def cleaner(self) -> DeadRabbitCleaner:
        return self._cleaner(self)


class FatteningRabbitCleanerMixin(RabbitCleanerMixin):
    _cleaner = FatteningRabbitCleaner

    @property
    def cleaner(self) -> FatteningRabbitCleaner:
        return self._cleaner(self)


class BunnyCleanerMixin(RabbitCleanerMixin):
    _cleaner = BunnyCleaner

    @property
    def cleaner(self) -> BunnyCleaner:
        return self._cleaner(self)


class MotherRabbitCleanerMixin(RabbitCleanerMixin):
    _cleaner = MotherRabbitCleaner

    @property
    def cleaner(self) -> MotherRabbitCleaner:
        return self._cleaner(self)


class FatherRabbitCleanerMixin(RabbitCleanerMixin):
    _cleaner = FatherRabbitCleaner

    @property
    def cleaner(self) -> FatherRabbitCleaner:
        return self._cleaner(self)
