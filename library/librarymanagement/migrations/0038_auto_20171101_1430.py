# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 09:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('librarymanagement', '0037_auto_20171101_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customusers',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='customusers',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='id',
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='user',
        ),

        migrations.AlterField(
            model_name='lendrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 14, 29, 54, 173077)),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 14, 29, 54, 175077)),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),

    ]
