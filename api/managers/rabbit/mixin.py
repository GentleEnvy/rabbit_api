from api.managers.rabbit._time_manager import *
from api.managers.base import BaseTimeManagerMixin

__all__ = [
    'RabbitTimeManagerMixin', 'FatteningRabbitTimeManagerMixin', 'BunnyTimeManagerMixin',
    'MotherRabbitTimeManagerMixin', 'FatherRabbitTimeManagerMixin'
]


class RabbitTimeManagerMixin(BaseTimeManagerMixin):
    _time_manager = RabbitTimeManager

    def time_manager(self, time=None) -> RabbitTimeManager:
        return super().time_manager(time)


class FatteningRabbitTimeManagerMixin(BaseTimeManagerMixin):
    _time_manager = FatherRabbitTimeManager

    def time_manager(self, time=None) -> FatherRabbitTimeManager:
        return super().time_manager(time)


class BunnyTimeManagerMixin(BaseTimeManagerMixin):
    _time_manager = BunnyTimeManager

    def time_manager(self, time=None) -> BunnyTimeManager:
        return super().time_manager(time)


class MotherRabbitTimeManagerMixin(BaseTimeManagerMixin):
    _time_manager = MotherRabbitTimeManager

    def time_manager(self, time=None) -> MotherRabbitTimeManager:
        return super().time_manager(time)


class FatherRabbitTimeManagerMixin(BaseTimeManagerMixin):
    _time_manager = FatherRabbitTimeManager

    def time_manager(self, time=None) -> FatherRabbitTimeManager:
        return super().time_manager(time)
