# Generated by Django 3.2.4 on 2021-07-04 20:17
import datetime

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motherrabbit',
            name='is_pregnant',
        ),
        migrations.RemoveField(
            model_name='motherrabbithistory',
            name='is_pregnant',
        ),
        migrations.CreateModel(
            name='PregnancyInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(default=datetime.datetime.utcnow)),
                ('is_pregnant', models.BooleanField()),
                ('mother_rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.motherrabbit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('father_rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatherrabbit')),
                ('mother_rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.motherrabbit')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
