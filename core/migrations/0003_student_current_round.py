# Generated by Django 2.1.5 on 2019-01-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190120_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='current_round',
            field=models.IntegerField(default=1),
        ),
    ]
