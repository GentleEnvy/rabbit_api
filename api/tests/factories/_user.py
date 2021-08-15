from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

__all__ = ['UserFactory']


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
    
    username = 'envy'
    password = 'coolpass'
