# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-16 21:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chameleon', '0006_auto_20200713_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproperties',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProperties',
        ),
    ]
