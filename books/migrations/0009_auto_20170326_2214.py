# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20170326_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
