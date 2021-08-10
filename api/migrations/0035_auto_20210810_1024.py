# Generated by Django 3.2.4 on 2021-08-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20210810_0005'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bunny',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='deadrabbit',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='fatherrabbit',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='fatteningrabbit',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='motherrabbit',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='rabbit',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='historicalbunny',
            name='last_weighting',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalfatherrabbit',
            name='last_weighting',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalfatteningrabbit',
            name='last_weighting',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalmotherrabbit',
            name='last_weighting',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rabbit',
            name='last_weighting',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]