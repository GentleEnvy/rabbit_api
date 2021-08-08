from django.db import models
from django.forms import model_to_dict

__all__ = ['BaseModel']


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
