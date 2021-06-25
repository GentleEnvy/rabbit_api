from django.db import models

__all__ = ['BaseModel']


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
