# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-27 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algo_app', '0002_auto_20180926_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('lessons', models.ManyToManyField(related_name='questions', to='algo_app.Lesson')),
                ('sub_lessons', models.ManyToManyField(related_name='questions', to='algo_app.Sub_lesson')),
            ],
        ),
    ]