# Generated by Django 3.2.4 on 2021-07-31 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_slaughterinspectiontask_weights'),
    ]

    operations = [
        migrations.AddField(
            model_name='rabbithistory',
            name='weight',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
