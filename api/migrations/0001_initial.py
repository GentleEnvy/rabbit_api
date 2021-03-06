# Generated by Django 3.2.4 on 2021-07-04 17:01
import datetime

import api.services.model.rabbit.managers.mixins
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(4)])),
                ('number', models.IntegerField()),
                ('letter', models.CharField(choices=[('а', 'LETTER_A'), ('б', 'LETTER_B'), ('в', 'LETTER_V'), ('г', 'LETTER_G')], default='а', max_length=1)),
                ('status', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('C', 'NEED_CLEAN'), ('R', 'NEED_REPAIR')], default='', max_length=3)),
            ],
            options={
                'unique_together': {('farm_number', 'number', 'letter')},
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.utcnow)),
                ('is_completed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rabbit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(default=datetime.datetime.utcnow)),
                ('is_male', models.BooleanField(blank=True, null=True)),
                ('is_vaccinated', models.BooleanField(default=False)),
                ('current_type', models.CharField(choices=[('D', 'TYPE_DEAD'), ('B', 'TYPE_BUNNY'), ('F', 'TYPE_FATTENING'), ('P', 'TYPE_FATHER'), ('M', 'TYPE_MOTHER')], default='B', max_length=1)),
                ('warning_status', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('NE', 'NOT_EAT'), ('ND', 'NOT_DRINK'), ('GS', 'GOT_SICK')], default='', max_length=8)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, api.services.model.rabbit.managers.mixins.RabbitManagerMixin),
        ),
        migrations.CreateModel(
            name='RabbitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_vaccinated', models.BooleanField(blank=True, default=None, null=True)),
                ('current_type', models.TextField(blank=True, default=None, null=True)),
                ('warning_status', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.utcnow)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bunny',
            fields=[
                ('rabbit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=(api.services.model.rabbit.managers.mixins.BunnyManagerMixin, 'api.rabbit'),
        ),
        migrations.CreateModel(
            name='DeadRabbit',
            fields=[
                ('rabbit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbit')),
                ('death_date', models.DateField(auto_now_add=True)),
                ('death_cause', models.CharField(choices=[('S', 'CAUSE_SLAUGHTER'), ('M', 'CAUSE_MOTHER'), ('I', 'CAUSE_ILLNESS'), ('D', 'CAUSE_DISEASE'), ('H', 'CAUSE_HEAT'), ('C', 'CAUSE_COOLING'), ('E', 'CAUSE_EXTRA')], max_length=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('api.rabbit',),
        ),
        migrations.CreateModel(
            name='FatherRabbit',
            fields=[
                ('rabbit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=(api.services.model.rabbit.managers.mixins.FatherRabbitManagerMixin, 'api.rabbit'),
        ),
        migrations.CreateModel(
            name='FatteningCage',
            fields=[
                ('cage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.cage')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.cage',),
        ),
        migrations.CreateModel(
            name='FatteningRabbit',
            fields=[
                ('rabbit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbit')),
                ('cage', models.ForeignKey(limit_choices_to={'status': []}, on_delete=django.db.models.deletion.PROTECT, to='api.fatteningcage')),
            ],
            options={
                'abstract': False,
            },
            bases=(api.services.model.rabbit.managers.mixins.FatteningRabbitManagerMixin, 'api.rabbit'),
        ),
        migrations.CreateModel(
            name='MatingPlan',
            fields=[
                ('plan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.plan')),
                ('number_pairs', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('api.plan',),
        ),
        migrations.CreateModel(
            name='MotherCage',
            fields=[
                ('cage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.cage')),
                ('is_parallel', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('api.cage',),
        ),
        migrations.CreateModel(
            name='MotherRabbit',
            fields=[
                ('rabbit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbit')),
                ('is_pregnant', models.BooleanField(default=False)),
                ('cage', models.ForeignKey(limit_choices_to={'status': []}, on_delete=django.db.models.deletion.PROTECT, to='api.cage')),
            ],
            options={
                'abstract': False,
            },
            bases=(api.services.model.rabbit.managers.mixins.MotherRabbitManagerMixin, 'api.rabbit'),
        ),
        migrations.CreateModel(
            name='SlaughterPlan',
            fields=[
                ('plan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.plan')),
                ('number_rabbits', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('api.plan',),
        ),
        migrations.CreateModel(
            name='BeforeSlaughterInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(default=datetime.datetime.utcnow)),
                ('weight', models.FloatField()),
                ('delay', models.IntegerField(blank=True, null=True)),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rabbit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlaughterTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.fatteningrabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.AddField(
            model_name='rabbit',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.fatherrabbit'),
        ),
        migrations.AddField(
            model_name='rabbit',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.motherrabbit'),
        ),
        migrations.CreateModel(
            name='MotherRabbitHistory',
            fields=[
                ('rabbithistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbithistory')),
                ('cage', models.IntegerField(blank=True, default=None, null=True)),
                ('is_pregnant', models.BooleanField(blank=True, default=None, null=True)),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.motherrabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.rabbithistory',),
        ),
        migrations.CreateModel(
            name='MatingTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.task')),
                ('father_rabbit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.fatherrabbit')),
                ('mother_rabbit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.motherrabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.task',),
        ),
        migrations.CreateModel(
            name='FatteningRabbitHistory',
            fields=[
                ('rabbithistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbithistory')),
                ('cage', models.IntegerField(blank=True, default=None, null=True)),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatteningrabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.rabbithistory',),
        ),
        migrations.CreateModel(
            name='FatherRabbitHistory',
            fields=[
                ('rabbithistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbithistory')),
                ('cage', models.IntegerField(blank=True, default=None, null=True)),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fatherrabbit')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.rabbithistory',),
        ),
        migrations.AddField(
            model_name='fatherrabbit',
            name='cage',
            field=models.ForeignKey(limit_choices_to={'status': []}, on_delete=django.db.models.deletion.PROTECT, to='api.fatteningcage'),
        ),
        migrations.CreateModel(
            name='BunnyHistory',
            fields=[
                ('rabbithistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.rabbithistory')),
                ('cage', models.IntegerField(blank=True, default=None, null=True)),
                ('rabbit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bunny')),
            ],
            options={
                'abstract': False,
            },
            bases=('api.rabbithistory',),
        ),
        migrations.AddField(
            model_name='bunny',
            name='cage',
            field=models.ForeignKey(limit_choices_to={'status': []}, on_delete=django.db.models.deletion.PROTECT, to='api.mothercage'),
        ),
    ]
