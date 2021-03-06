# Generated by Django 3.2.4 on 2021-07-10 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_motherrabbit_cage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beforeslaughterinspection',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='bunny',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='bunnyhistory',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='cage',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='deadrabbit',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='fatherrabbit',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='fatherrabbithistory',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='fatteningcage',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='fatteningrabbit',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='fatteningrabbithistory',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='mating',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='matingplan',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='matingtask',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='mothercage',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='motherrabbit',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='motherrabbithistory',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='plan',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='pregnancyinspection',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='rabbit',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='rabbithistory',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='slaughterplan',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='slaughtertask',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['pk']},
        ),
    ]
