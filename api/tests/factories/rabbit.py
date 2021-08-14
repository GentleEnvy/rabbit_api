import factory
from factory.django import DjangoModelFactory

from api.models import *
from api.tests.factories.breed import BreedFactory
from api.tests.factories.cage import MotherCageFactory, FatteningCageFactory

__all__ = [
    'MotherRabbitFactory', 'FatherRabbitFactory', 'BunnyFactory', 'FatteningRabbitFactory'
]


class MotherRabbitFactory(DjangoModelFactory):
    class Meta:
        model = MotherRabbit
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(MotherCageFactory)
    is_male = False
    is_vaccinated = True


class FatherRabbitFactory(DjangoModelFactory):
    class Meta:
        model = FatherRabbit
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(FatteningCageFactory)
    is_male = True
    is_vaccinated = True


class BunnyFactory(DjangoModelFactory):
    class Meta:
        model = Bunny
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(MotherCageFactory)
    mother = factory.SubFactory(MotherRabbitFactory)
    father = factory.SubFactory(FatherRabbitFactory)


class FatteningRabbitFactory(DjangoModelFactory):
    class Meta:
        model = FatteningRabbit
    
    breed = factory.SubFactory(BreedFactory)
    cage = factory.SubFactory(FatteningCageFactory)
    mother = factory.SubFactory(MotherRabbitFactory)
    father = factory.SubFactory(FatherRabbitFactory)
