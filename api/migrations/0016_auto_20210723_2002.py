# Generated by Django 3.2.4 on 2021-07-23 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_typegroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date',
        ),
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='is_confirmed',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='matingtask',
            name='father_rabbit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatherrabbit'),
        ),
        migrations.AlterField(
            model_name='matingtask',
            name='mother_rabbit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.motherrabbit'),
        ),
        migrations.AlterField(
            model_name='slaughtertask',
            name='rabbit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rabbit'),
        ),
        migrations.CreateModel(
            name='VaccinationTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatteningcage')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.CreateModel(
            name='ToReproductionTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('cage_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cage')),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatteningrabbit')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.CreateModel(
            name='SlaughterInspectionTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatteningcage')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.CreateModel(
            name='FatteningSlaughterTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('cage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatteningcage')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.CreateModel(
            name='BunnyJiggingTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('cage_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.mothercage')),
                ('female_cage_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bunnyjiggingtask_by_female_set', to='api.fatteningcage')),
                ('male_cage_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bunnyjiggingtask_by_male_set', to='api.fatteningcage')),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
            bases=('api.task',),
        ),
    ]
