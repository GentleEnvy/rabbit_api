from api.models import *
from datetime import date, timedelta


def next_delivery_date():
    amount_of_rabbits_that_need_food = len(FatherRabbit.objects.all()) + \
                                       len(MotherRabbit.objects.all()) + \
                                       len(FatteningRabbit.objects.all())
    pass
