from api.services.feeding import *
from api.services.prediction.rabbit import *


class MotherFeeding(FeedingService):
    def __init__(self):
        super(MotherFeeding, self).__init__()
    
    def days_left_for_feed_stocks(self) -> int:
        feeding_mothers = self.mothers_with_prognosis()
        days_left = 0
        feed_left = CommonFeeds.objects.aggregate(
            Sum('stocks_change')
        ).get('stocks_change__sum') * self.feed_bag_weight
        while feed_left > 0 and days_left < self.days_for_plan:
            feed_left -= feeding_mothers[days_left] * self.normal_daily_consumption
            days_left += 1
        
        return days_left
    
    def mothers_with_prognosis(self) -> list:
        predictor = PredictionRabbitService()
        mothers_for_each_day = predictor.predict(
            days=self.days_for_plan,
            every_day=True
        )
        feeding_mothers_for_each_day = []
        for day in range(self.days_for_plan):
            mothers_count = 0
            for mother_rabbit in mothers_for_each_day[day].mother_rabbits:
                if 'FB' in mother_rabbit.status:
                    mothers_count += 1
            feeding_mothers_for_each_day.append(mothers_count)
        return feeding_mothers_for_each_day
