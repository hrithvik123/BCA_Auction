# Generated by Django 3.2 on 2021-04-06 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auto_20210405_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 7, 1, 56, 0, 496488)),
        ),
    ]
