# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 05:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20170326_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_date',
            field=models.DateField(default=datetime.date(2017, 3, 26)),
        ),
    ]
