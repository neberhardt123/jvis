# Generated by Django 3.2 on 2021-09-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_boxservice_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boxservice',
            options={'ordering': ['port']},
        ),
        migrations.AlterField(
            model_name='boxservice',
            name='port',
            field=models.IntegerField(blank=True),
        ),
    ]