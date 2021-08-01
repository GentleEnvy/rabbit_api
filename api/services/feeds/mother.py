from api.managers import MotherRabbitManager
from api.models import *
from api.services.feeds.base import *

__all__ = ['MotherFeedingService']


class MotherFeedingService(FeedingService):
    _feeds_model = MotherFeeds
    
    def _rabbits_with_prognosis(self):
        mothers_for_each_day = self._get_predictions()
        feeding_mothers_for_each_day = []
        for day in range(self.days_for_plan):
            mothers_count = 0
            for mother_rabbit in mothers_for_each_day[day].mother_rabbits:
                if MotherRabbitManager.STATUS_FEEDS_BUNNY in mother_rabbit.status:
                    mothers_count += 1
            feeding_mothers_for_each_day.append(mothers_count)
        return feeding_mothers_for_each_day
