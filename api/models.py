from django.db import models


class Cage(models.Model):
    farm_number = models.IntegerField()
    number = models.IntegerField()
    letter = models.CharField(max_length=1, null=False, blank=False)

    class Meta:
        unique_together = ('farm_number', 'number', 'letter')


class FatteningCage(Cage):
    max_capacity = models.IntegerField(default=1)


class MotherCage(Cage):
    pass


class Rabbit(models.Model):
    birthdate = models.DateTimeField(auto_now_add=True)
    mother = models.ForeignKey('MotherRabbit', on_delete=models.SET_NULL, null=True)
    father = models.ForeignKey('FatherRabbit', on_delete=models.SET_NULL, null=True)


class FatteningRabbit(Rabbit):
    is_male = models.BooleanField(null=True)
    cage = models.ForeignKey(FatteningCage, on_delete=models.PROTECT)


class Bunny(Rabbit):
    need_jigging = models.BooleanField(default=False, null=True)
    cage = models.ForeignKey(MotherCage, on_delete=models.PROTECT)


class MotherRabbit(Rabbit):
    mother_status = models.CharField(
        choices=(
            (PREGNANT := 'P', 'PREGNANT'),
            (FEEDS := 'F', 'FEEDS')
        ),
        max_length=1, null=True, blank=False
    )
    last_childbirth = models.DateField(null=True, blank=False)
    cage = models.ForeignKey(MotherCage, on_delete=models.PROTECT)


class FatherRabbit(Rabbit):
    is_resting = models.BooleanField(default=True)
    cage = models.ForeignKey(Cage, on_delete=models.PROTECT)
