# Generated by Django 3.2 on 2021-09-19 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_alter_box_orderedip'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='comeback',
            field=models.BooleanField(default=False, verbose_name='Come back to this box'),
        ),
        migrations.AddField(
            model_name='box',
            name='unrelated',
            field=models.BooleanField(default=False),
        ),
    ]
