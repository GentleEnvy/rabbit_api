from django.db import models

__all__ = ['BaseModel']

from django.forms import model_to_dict


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ListenDiffModel(BaseModel):
    class Meta:
        abstract = True

    listening_fields: tuple[str] = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__real = self.__listening_dict

    @property
    def diff(self):
        real_dict = self.__real
        listening_dict = self.__listening_dict
        diffs = {
            field: new_value
            for field, new_value in listening_dict.items()
            if new_value != real_dict[field]
        }
        return diffs

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__real = self.__listening_dict

    @property
    def __listening_fields(self) -> tuple[str]:
        if self.listening_fields == '__all__':
            return tuple(self._meta.fields)
        return self.listening_fields

    @property
    def __listening_dict(self):
        return model_to_dict(self, fields=self.__listening_fields)
