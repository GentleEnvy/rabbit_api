from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

__all__ = ['BaseCage', 'FatteningCage', 'MotherCage']


class BaseCage(models.Model):
    farm_number = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(4)]
    )
    number = models.IntegerField()
    letter = models.CharField(max_length=1, default='а')
    status = MultiSelectField(
        choices=(
            (NEED_CLEAN := 'C', 'NEED_CLEAN'),
            (NEED_REPAIR := 'R', 'NEED_REPAIR')
        ),
        blank=True, default='', max_choices=2
    )

    class Meta:
        unique_together = ('farm_number', 'number', 'letter')


class FatteningCage(BaseCage):
    pass


class MotherCage(BaseCage):
    is_parallel = models.BooleanField(default=False)
