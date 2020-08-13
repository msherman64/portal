# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-12 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing_portal', '0008_author_name_affiliation'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifactversion',
            name='deposition_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifactversion',
            name='deposition_repo',
            field=models.CharField(choices=[(b'zenodo', b'Zenodo'), (b'chameleon', b'Chameleon'), (b'git', b'Git')], default=b'chameleon', max_length=24),
        ),
        migrations.AlterField(
            model_name='artifactversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
