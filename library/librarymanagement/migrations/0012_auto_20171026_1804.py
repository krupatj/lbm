# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-26 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarymanagement', '0011_auto_20171023_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='authors', to='librarymanagement.Author'),
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='final_decision',
            field=models.CharField(choices=[('Approve', 'Approve'), ('Reject', 'Reject'), ('On Hold', 'On Hold')], max_length=1),
        ),
        migrations.AlterField(
            model_name='lendrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=1),
        ),
        migrations.AlterField(
            model_name='photo',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='librarymanagement.Book'),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='final_decision',
            field=models.CharField(choices=[('Approve', 'Approve'), ('Reject', 'Reject'), ('On Hold', 'On Hold')], max_length=1),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=1),
        ),
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='librarymanagement.Book'),
        ),
    ]