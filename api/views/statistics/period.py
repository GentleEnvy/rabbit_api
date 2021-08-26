from api.views.statistics.base import BasePeriodStatisticView

__all__ = [
    'SlaughtersStatisticView', 'DeathsStatisticView', 'BunnyJigsStatisticView',
    'MatingsStatisticView'
]


class SlaughtersStatisticView(BasePeriodStatisticView):
    def _get(self, service):
        return service.slaughters()


class DeathsStatisticView(BasePeriodStatisticView):
    def _get(self, service):
        return service.deaths()


class BunnyJigsStatisticView(BasePeriodStatisticView):
    def _get(self, service):
        return service.bunny_jigs()


class MatingsStatisticView(BasePeriodStatisticView):
    def _get(self, service):
        return service.matings()
