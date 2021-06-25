from django.db import models

__all__ = ['BaseModel']


class BaseModel(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
