# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-12 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing_portal', '0010_migrate_zenodo_depositions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifact',
            name='image',
        ),
        migrations.RemoveField(
            model_name='artifact',
            name='launchable',
        ),
        migrations.AlterField(
            model_name='artifact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.RemoveField(
            model_name='artifactversion',
            name='doi',
        ),
    ]
