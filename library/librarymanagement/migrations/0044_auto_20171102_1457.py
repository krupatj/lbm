# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-02 09:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
       
    ]

    operations = [
        migrations.AlterField(
            model_name='lendrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 2, 14, 57, 58, 474211)),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 2, 14, 57, 58, 476211)),
        ),
    ]
