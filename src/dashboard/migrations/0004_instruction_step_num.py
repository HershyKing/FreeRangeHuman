# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20171211_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='step_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]