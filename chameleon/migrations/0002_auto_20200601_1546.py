# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-01 20:46


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chameleon', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userproperties',
            old_name='is_pi_eligible',
            new_name='is_pi',
        ),
    ]
