import factory
from factory.django import DjangoModelFactory

from api.models import *

__all__ = ['FatteningCageFactory', 'MotherCageFactory']


def _seq():
    n = 0
    while True:
        n += 1
        yield n


_number_gen = _seq()


class _CageFactory(DjangoModelFactory):
    farm_number = 2
    number = factory.Sequence(lambda _: next(_number_gen))


class FatteningCageFactory(_CageFactory):
    class Meta:
        model = FatteningCage


class MotherCageFactory(_CageFactory):
    class Meta:
        model = MotherCage
