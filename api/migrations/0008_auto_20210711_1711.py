# Generated by Django 3.2.4 on 2021-07-11 17:11
import datetime

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210710_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deadrabbit',
            name='death_date',
        ),
        migrations.AddField(
            model_name='deadrabbit',
            name='death_day',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
