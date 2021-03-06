# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 06:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0022_auto_20171101_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='LendRequestForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(default=datetime.datetime(2017, 11, 1, 11, 47, 20, 969830))),
                ('book', models.ManyToManyField(related_name='userbooks', to='librarymanagement.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.Client')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnRequestForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(default=datetime.datetime(2017, 11, 1, 11, 47, 20, 971831))),
                ('book', models.ManyToManyField(related_name='userbooks_return', to='librarymanagement.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.Client')),
            ],
        ),
    ]
