# Generated by Django 3.2 on 2021-09-05 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_box_pwned'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='boxservice',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
