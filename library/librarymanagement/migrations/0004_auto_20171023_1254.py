# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 07:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0003_auto_20171023_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lendrequest',
            name='request_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 23, 12, 54, 14, 520588)),
        ),
    ]