# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 08:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0031_auto_20171101_1358'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='CustomUsers',
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 13, 59, 53, 687046)),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 13, 59, 53, 689046)),
        ),
    ]
