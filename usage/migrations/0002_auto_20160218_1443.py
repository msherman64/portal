# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downtime',
            name='nodes_down',
            field=models.IntegerField(verbose_name=b'Down nodes'),
            preserve_default=True,
        ),
    ]
