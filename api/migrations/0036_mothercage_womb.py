# Generated by Django 3.2.4 on 2021-08-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20210810_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='mothercage',
            name='womb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.mothercage'),
        ),
    ]
