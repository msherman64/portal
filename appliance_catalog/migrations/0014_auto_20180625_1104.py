# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliance_catalog', '0013_auto_20171006_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliance',
            name='restrict_to_projects',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appliance',
            name='shared_from_horizon',
            field=models.BooleanField(default=False),
        ),
    ]
