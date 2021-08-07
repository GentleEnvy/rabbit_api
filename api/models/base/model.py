from django.db import models
from django.forms import model_to_dict

__all__ = ['BaseModel', 'ListenDiffModel']


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ListenDiffModel(BaseModel):
    class Meta(BaseModel.Meta):
        abstract = True
    
    listening_fields: tuple[str, ...] = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._real = self._changes_dict
    
    @property
    def diff(self):
        if self.id is None:
            return self._changes_dict
        real_dict = self._real
        changes_dict = self._changes_dict
        diffs = {
            field: real_dict.get(field)
            for field, new_value in changes_dict.items()
            if new_value != real_dict.get(field)
        }
        return diffs
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._real = self._changes_dict
    
    @property
    def __listening_fields(self) -> tuple[str, ...]:
        if self.listening_fields == '__all__':
            return tuple(field.name for field in self._meta.fields)
        return self.listening_fields
    
    @property
    def _changes_dict(self):
        return model_to_dict(self, fields=self.__listening_fields)
