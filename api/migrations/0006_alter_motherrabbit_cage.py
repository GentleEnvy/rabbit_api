# Generated by Django 3.2.4 on 2021-07-09 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210708_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motherrabbit',
            name='cage',
            field=models.ForeignKey(limit_choices_to={'status': []}, on_delete=django.db.models.deletion.PROTECT, to='api.mothercage'),
        ),
    ]