# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chameleon_mailman', '0002_auto_20150521_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailmansubscription',
            name='user',
            field=models.ForeignKey(related_name='subscriptions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
