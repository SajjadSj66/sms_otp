# Generated by Django 5.1.3 on 2024-11-26 11:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getotp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='valid_form',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 26, 11, 10, 36, 786246, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 26, 11, 12, 36, 786246, tzinfo=datetime.timezone.utc)),
        ),
    ]
