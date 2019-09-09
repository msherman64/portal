# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webinar_registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='registration_limit',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
