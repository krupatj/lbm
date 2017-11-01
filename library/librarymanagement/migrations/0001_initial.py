# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-20 10:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField(null=True)),
                ('country', models.CharField(max_length=30)),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('stock_count', models.IntegerField()),
                ('authors', models.ManyToManyField(to='librarymanagement.Author')),
            ],
        ),
        migrations.CreateModel(
            name='LendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(default=datetime.datetime(2017, 10, 20, 16, 10, 41, 162125))),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], max_length=1)),
                ('final_decision', models.CharField(choices=[('A', 'Approve'), ('R', 'Reject')], max_length=1)),
                ('book', models.ManyToManyField(to='librarymanagement.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('book_title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], max_length=1)),
                ('final_decision', models.CharField(choices=[('A', 'Approve'), ('R', 'Reject')], max_length=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=30)),
                ('review', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('phone_number', models.IntegerField()),
                ('email_id', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.User'),
        ),
        migrations.AddField(
            model_name='returnrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.User'),
        ),
        migrations.AddField(
            model_name='lendrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarymanagement.User'),
        ),
        migrations.AddField(
            model_name='book',
            name='photos',
            field=models.ManyToManyField(to='librarymanagement.Photo'),
        ),
        migrations.AddField(
            model_name='book',
            name='reviews',
            field=models.ManyToManyField(to='librarymanagement.Review'),
        ),
    ]