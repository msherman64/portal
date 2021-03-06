# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-28 19:31


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProperties',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_pi_eligible', models.BooleanField(default=False)),
            ],
        ),
    ]
