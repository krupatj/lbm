# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0029_auto_20171101_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lendrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 13, 18, 352685)),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 13, 18, 354685)),
        ),
    ]
