# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 02:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 26, 19, 17, 7, 312000)),
        ),
    ]
