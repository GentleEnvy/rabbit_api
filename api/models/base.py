from django.db import models
from django.forms import model_to_dict

__all__ = ['BaseModel', 'BaseHistoryModel', 'BaseHistoricalModel']


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ListenDiffModel(BaseModel):
    class Meta:
        abstract = True

    listening_fields: tuple[str, ...] = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._real = self._changes_dict
        print(f'{self._real = }')

    @property
    def diff(self):
        real_dict = self._real
        print(f'{real_dict = }')
        changes_dict = self._changes_dict
        print(f'{changes_dict = }')
        diffs = {
            field: new_value
            for field, new_value in changes_dict.items()
            if new_value != real_dict[field]
        }
        print(f'{diffs = }')
        return diffs

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._real = self._changes_dict

    @property
    def __listening_fields(self) -> tuple[str, ...]:
        print(f'{self.listening_fields = }')
        if self.listening_fields == '__all__':
            return tuple(field.name for field in self._meta.fields)
        return self.listening_fields

    @property
    def _changes_dict(self):
        return model_to_dict(self, fields=self.__listening_fields)


class BaseHistoryModel(models.Model):
    class Meta:
        abstract = True

    historical_name: str
    time_name: str = 'time'


class BaseHistoricalModel(ListenDiffModel):
    class Meta:
        abstract = True

    history_model: BaseHistoryModel

    @property
    def listening_fields(self) -> tuple[str, ...]:
        history_fields = {field.name for field in self.history_model._meta.fields}
        if 'id' in history_fields:
            history_fields.remove('id')
        if self.history_model.historical_name in history_fields:
            history_fields.remove(self.history_model.historical_name)
        if self.history_model.time_name in history_fields:
            history_fields.remove(self.history_model.time_name)
        return tuple(history_fields)

    def save(self, *args, **kwargs):
        diff = self.diff
        history_fields = {field.name for field in self.history_model._meta.fields}
        try:
            history_fields.remove('id')
        except KeyError:
            pass
        if diff:
            new_dict = {
                field: new_value
                for field, new_value in diff.items()
                if field in history_fields
            }
        else:
            try:
                self.__class__.objects.get(pk=self.pk)
                return super().save(*args, **kwargs)
            except self.DoesNotExist:
                new_dict = {
                    field: new_value
                    for field, new_value in model_to_dict(self).items()
                    if field in history_fields
                }
        super().save(*args, **kwargs)
        self.history_model.objects.create(
            **(new_dict | {self.history_model.historical_name: self})
        )
