from api.services.model.rabbit.managers._manager import *

__all__ = [
    'RabbitManagerMixin', 'FatteningRabbitManagerMixin', 'BunnyManagerMixin',
    'MotherRabbitManagerMixin', 'FatherRabbitManagerMixin'
]


class RabbitManagerMixin:
    Manager = RabbitManager
    
    @property
    def manager(self) -> RabbitManager:
        return self.Manager(self)


class FatteningRabbitManagerMixin(RabbitManagerMixin):
    Manager = FatteningRabbitManager
    
    @property
    def manager(self) -> FatteningRabbitManager:
        return self.Manager(self)


class BunnyManagerMixin(RabbitManagerMixin):
    Manager = BunnyManager
    
    @property
    def manager(self) -> BunnyManager:
        return self.Manager(self)


class MotherRabbitManagerMixin(RabbitManagerMixin):
    Manager = MotherRabbitManager
    
    @property
    def manager(self) -> MotherRabbitManager:
        return self.Manager(self)


class FatherRabbitManagerMixin(RabbitManagerMixin):
    Manager = FatherRabbitManager
    
    @property
    def manager(self) -> FatherRabbitManager:
        return self.Manager(self)
