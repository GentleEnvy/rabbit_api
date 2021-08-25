from api.views.statistics.base import BaseTimeStatisticView

__all__ = [
    'RabbitsStatisticView', 'FatteningsStatisticView', 'MothersStatisticView',
    'FathersStatisticView', 'BunniesStatisticView'
]


class RabbitsStatisticView(BaseTimeStatisticView):
    def _get(self, service):
        return service.rabbits()


class FatteningsStatisticView(BaseTimeStatisticView):
    def _get(self, service):
        return service.fattenings()


class MothersStatisticView(BaseTimeStatisticView):
    def _get(self, service):
        return service.mothers()


class FathersStatisticView(BaseTimeStatisticView):
    def _get(self, service):
        return service.fathers()


class BunniesStatisticView(BaseTimeStatisticView):
    def _get(self, service):
        return service.bunnies()
