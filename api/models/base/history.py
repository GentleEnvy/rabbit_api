from django.db import models
from django.forms import model_to_dict

from api.models.base.model import ListenDiffModel, BaseModel

__all__ = ['BaseHistoryModel', 'BaseHistoricalModel']


class BaseHistoryModel(BaseModel):
    class Meta(BaseModel.Meta):
        abstract = True
    
    historical_name: str
    time_name: str = 'time'
    replace_fields: dict = {}
    
    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)


class BaseHistoricalModel(ListenDiffModel):
    class Meta(ListenDiffModel.Meta):
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
        for old_filed, new_field in self.history_model.replace_fields.items():
            try:
                new_dict[new_field] = new_dict.pop(old_filed)
            except KeyError:
                pass
        super().save(*args, **kwargs)
        self.history_model.objects.create(
            **(new_dict | {self.history_model.historical_name: self})
        )
