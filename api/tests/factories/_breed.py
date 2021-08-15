from factory.django import DjangoModelFactory

from api.models import Breed

__all__ = ['BreedFactory']


class BreedFactory(DjangoModelFactory):
    class Meta:
        model = Breed
        django_get_or_create = ['title']
    
    title = 'Паннон'
