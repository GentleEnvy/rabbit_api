# Generated by Django 3.2.4 on 2021-07-24 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0016_auto_20210723_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bunnyjiggingtask',
            name='female_cage_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bunnyjiggingtask_by_female_set', to='api.fatteningcage'),
        ),
        migrations.AlterField(
            model_name='bunnyjiggingtask',
            name='male_cage_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bunnyjiggingtask_by_male_set', to='api.fatteningcage'),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_confirmed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='toreproductiontask',
            name='cage_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cage'),
        ),
    ]