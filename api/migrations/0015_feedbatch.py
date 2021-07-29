# Generated by Django 3.2.4 on 2021-07-18 22:35
import datetime

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210717_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateField(default=datetime.datetime.utcnow)),
                ('total_bags_number', models.IntegerField()),
                ('bags_left', models.IntegerField()),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
    ]
