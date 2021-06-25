from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

__all__ = ['Cage', 'FatteningCage', 'MotherCage']


class Cage(models.Model):
    farm_number = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(4)]
    )
    number = models.IntegerField()
    letter = models.CharField(
        choices=(
            (LETTER_A := 'а', 'LETTER_A'),
            (LETTER_B := 'б', 'LETTER_B'),
            (LETTER_V := 'в', 'LETTER_V'),
            (LETTER_G := 'г', 'LETTER_G')
        ),
        max_length=1, default=LETTER_A
    )
    status = MultiSelectField(
        choices=(
            (NEED_CLEAN := 'C', 'NEED_CLEAN'),
            (NEED_REPAIR := 'R', 'NEED_REPAIR')
        ),
        blank=True, default='', max_choices=2
    )

    class Meta:
        unique_together = ('farm_number', 'number', 'letter')


class FatteningCage(Cage):
    pass


class MotherCage(Cage):
    is_parallel = models.BooleanField(default=False)
