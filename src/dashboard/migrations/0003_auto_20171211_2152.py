# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 02:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20171209_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='step_num',
        ),
        migrations.AlterField(
            model_name='instruction',
            name='instruction',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together=set([('date', 'user')]),
        ),
    ]
