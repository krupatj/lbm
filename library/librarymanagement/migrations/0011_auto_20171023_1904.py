# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0010_auto_20171023_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='book_title',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='review',
            name='book_title',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
