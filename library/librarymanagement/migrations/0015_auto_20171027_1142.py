# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-27 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0014_auto_20171027_1016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnrequest',
            name='final_decision',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='status',
        ),
        migrations.AddField(
            model_name='returnrequest',
            name='return_status',
            field=models.CharField(choices=[('Received', 'Received'), ('Not Received', 'Not Received')], default='Not Received', max_length=30),
            preserve_default=False,
        ),
    ]