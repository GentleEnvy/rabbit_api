from api.managers.rabbit._manager import *
from api.managers.base import BaseManagerMixin

__all__ = [
    'RabbitManagerMixin', 'FatteningRabbitManagerMixin', 'BunnyManagerMixin',
    'MotherRabbitManagerMixin', 'FatherRabbitManagerMixin'
]


class RabbitManagerMixin(BaseManagerMixin):
    _manager = RabbitManager

    @property
    def manager(self) -> RabbitManager:
        return super().manager


class FatteningRabbitManagerMixin(BaseManagerMixin):
    _manager = FatteningRabbitManager

    @property
    def manager(self) -> FatherRabbitManager:
        return super().manager


class BunnyManagerMixin(BaseManagerMixin):
    _manager = BunnyManager

    @property
    def manager(self) -> BunnyManager:
        return super().manager


class MotherRabbitManagerMixin(BaseManagerMixin):
    _manager = MotherRabbitManager

    @property
    def manager(self) -> MotherRabbitManager:
        return super().manager


class FatherRabbitManagerMixin(BaseManagerMixin):
    _manager = FatherRabbitManager

    @property
    def manager(self) -> FatherRabbitManager:
        return super().manager
