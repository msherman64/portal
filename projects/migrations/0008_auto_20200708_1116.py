# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-08 16:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0007_auto_20200212_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldHierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_child', to='projects.Field')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_parent', to='projects.Field')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('nickname', models.CharField(max_length=255, unique=True)),
                ('charge_code', models.CharField(max_length=50)),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_field', to='projects.Field')),
                ('pi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_pi', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='tas_project_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_type', to='projects.Type'),
        ),
        migrations.AddField(
            model_name='publication',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_publication', to='projects.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='fieldhierarchy',
            unique_together=set([('parent', 'child')]),
        ),
    ]
