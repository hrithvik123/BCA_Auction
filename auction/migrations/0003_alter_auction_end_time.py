# Generated by Django 3.2 on 2021-05-10 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_alter_auction_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 18, 55, 21, 25802)),
        ),
    ]
