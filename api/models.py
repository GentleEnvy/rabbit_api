from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField


class Cage(models.Model):
    farm_number = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(4)]
    )
    number = models.IntegerField()
    letter = models.CharField(max_length=1, blank=True, default='')
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
    max_capacity = models.PositiveIntegerField(default=1)


class MotherCage(Cage):
    pass


class Rabbit(models.Model):
    birthdate = models.DateTimeField(auto_now_add=True)
    mother = models.ForeignKey(
        'MotherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )
    father = models.ForeignKey(
        'FatherRabbit', on_delete=models.SET_NULL, null=True, blank=True
    )


class FatteningRabbit(Rabbit):
    is_male = models.BooleanField(null=True, blank=True)
    cage = models.ForeignKey(FatteningCage, on_delete=models.PROTECT)


class Bunny(Rabbit):
    need_jigging = models.BooleanField(default=False)
    cage = models.ForeignKey(MotherCage, on_delete=models.PROTECT)


class MotherRabbit(Rabbit):
    status = MultiSelectField(
        choices=(
            (PREGNANT := 'P', 'PREGNANT'),
            (FEEDS := 'F', 'FEEDS')
        ),
        blank=True, default='', max_choices=2
    )
    last_childbirth = models.DateField(null=True, blank=True)
    cage = models.ForeignKey(MotherCage, on_delete=models.PROTECT)


class FatherRabbit(Rabbit):
    is_resting = models.BooleanField(default=True)
    cage = models.ForeignKey(Cage, on_delete=models.PROTECT)
