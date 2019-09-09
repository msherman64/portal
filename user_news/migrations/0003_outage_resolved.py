# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_news', '0002_auto_20150519_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='outage',
            name='resolved',
            field=models.BooleanField(default=False, verbose_name=b'resolved'),
            preserve_default=True,
        ),
    ]
