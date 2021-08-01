from api.managers import MotherRabbitManager
from api.models import *
from api.services.feeds.base import *

__all__ = ['FatteningFeedingService']


class FatteningFeedingService(FeedingService):
    _feeds_model = FatteningFeeds
    
    def _rabbits_with_prognosis(self):
        rabbits_for_each_day = self._get_predictions()
        feeding_rabbits_for_each_day = []
        for day in range(self.days_for_plan):
            rabbits_count = len(
                rabbits_for_each_day[day].fattening_rabbits
            ) + len(
                rabbits_for_each_day[day].father_rabbits
            )
            for mother_rabbit in rabbits_for_each_day[day].mother_rabbits:
                if MotherRabbitManager.STATUS_FEEDS_BUNNY not in mother_rabbit.status:
                    rabbits_count += 1
            feeding_rabbits_for_each_day.append(rabbits_count)
        return feeding_rabbits_for_each_day
