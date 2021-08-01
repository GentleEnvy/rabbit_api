from django.db.models import Sum

from api.models import Feeds
from api.services.prediction import PredictionRabbitService

__all__ = ['FeedingService']


class FeedingService:
    _feeds_model: Feeds
    
    FEED_BAG_WEIGHT = 25000
    NORMAL_DAILY_CONSUMPTION = 120
    INCREASED_DAILY_CONSUMPTION = 200
    DAYS_FOR_PROGNOSTICATION = 14
    MILK_AGE_FOR_BUNNY = 14
    
    def __init__(
        self,
        feed_bag_weight=FEED_BAG_WEIGHT,
        normal_daily_consumption=NORMAL_DAILY_CONSUMPTION,
        increased_daily_consumption=INCREASED_DAILY_CONSUMPTION,
        days_for_prognostication=DAYS_FOR_PROGNOSTICATION,
        milk_age_for_bunny=MILK_AGE_FOR_BUNNY,
    ):
        self.feed_bag_weight = feed_bag_weight
        self.normal_daily_consumption = normal_daily_consumption
        self.increased_daily_consumption = increased_daily_consumption
        self.days_for_plan = days_for_prognostication
        self.milk_age_for_bunny = milk_age_for_bunny
    
    def days_left_for_feed_stocks(self) -> int:
        feeding_rabbits = self._rabbits_with_prognosis()
        days_left = 0
        feed_left = self._feeds_model.objects.aggregate(
            Sum('stocks')
        ).get('stocks__sum') * self.feed_bag_weight
        while feed_left > 0 and days_left < self.days_for_plan:
            feed_left -= feeding_rabbits[days_left] * self.normal_daily_consumption
            days_left += 1
        
        return days_left
    
    def _get_predictions(self):
        predictor = PredictionRabbitService()
        return predictor.predict(
            days=self.days_for_plan,
            every_day=True
        )
    
    def _rabbits_with_prognosis(self) -> list[int]:
        raise NotImplementedError
