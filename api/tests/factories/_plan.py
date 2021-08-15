from factory.django import DjangoModelFactory

from api.models import *

__all__ = ['PlanFactory']


class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    quantity = 1
