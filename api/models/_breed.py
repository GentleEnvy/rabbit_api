from django.db import models

from api.models.base import BaseModel

__all__ = ['Breed']


class Breed(BaseModel):
    title = models.TextField()
