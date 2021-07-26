from django.contrib.auth.models import Group
from django.db import models

__all__ = ['TypeGroup']


class TypeGroup(Group):
    type = models.CharField(max_length=2)
