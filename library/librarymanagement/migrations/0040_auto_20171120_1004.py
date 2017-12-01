# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-20 04:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0039_merge_20171114_1659'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lendrequests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_return', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CustomUsers',
        ),
    ]