# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 06:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0024_auto_20171101_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lendrequestform',
            name='book',
        ),
        migrations.RemoveField(
            model_name='lendrequestform',
            name='user',
        ),
        migrations.RemoveField(
            model_name='returnrequestform',
            name='book',
        ),
        migrations.RemoveField(
            model_name='returnrequestform',
            name='user',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='date',
        ),
        migrations.AddField(
            model_name='returnrequest',
            name='return_request_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 5, 7, 248448)),
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='request_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 12, 5, 7, 246447)),
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lendrequests', to='librarymanagement.Client'),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_return', to='librarymanagement.Client'),
        ),
        migrations.DeleteModel(
            name='LendRequestForm',
        ),
        migrations.DeleteModel(
            name='ReturnRequestForm',
        ),
    ]
