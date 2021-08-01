from api.services.feeding import *
from api.services.prediction.rabbit import *


class CommonFeeding(FeedingService):
    def __init__(self):
        super(CommonFeeding, self).__init__()
    
    def days_left_for_feed_stocks(self) -> int:
        feeding_rabbits = self.rabbits_with_prognosis()
        days_left = 0
        feed_left = CommonFeeds.objects.aggregate(
            Sum('stocks_change')
        ).get('stocks_change__sum') * self.feed_bag_weight
        while feed_left > 0 and days_left < self.days_for_plan:
            feed_left -= feeding_rabbits[days_left] * self.normal_daily_consumption
            days_left += 1
        
        return days_left
    
    def rabbits_with_prognosis(self) -> list:
        predictor = PredictionRabbitService()
        rabbits_for_each_day = predictor.predict(
            days=self.days_for_plan,
            every_day=True
        )
        feeding_rabbits_for_each_day = []
        for day in range(self.days_for_plan):
            rabbits_count = len(
                rabbits_for_each_day[day].fattening_rabbits
            ) + len(
                rabbits_for_each_day[day].father_rabbits
            )
            for mother_rabbit in rabbits_for_each_day[day].mother_rabbits:
                if 'FB' not in mother_rabbit.status:
                    rabbits_count += 1
            feeding_rabbits_for_each_day.append(rabbits_count)
        return feeding_rabbits_for_each_day
