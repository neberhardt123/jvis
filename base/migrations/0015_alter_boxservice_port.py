# Generated by Django 3.2 on 2021-09-05 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_boxservice_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxservice',
            name='port',
            field=models.IntegerField(blank=True),
        ),
    ]
