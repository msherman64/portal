# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-12 20:32


from django.db import migrations


def migrate_to_deposition_fields(apps, schema_editor):
    ArtifactVersion = apps.get_model('sharing_portal', 'ArtifactVersion')

    # Existing versions were all stored on Zenodo, so we just migrate
    # them all under the same repo. The ID of a Zenodo deposition is its DOI.
    for version in ArtifactVersion.objects.all():
        version.deposition_repo = 'zenodo'
        version.deposition_id = version.doi
        version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sharing_portal', '0009_add_deposition_fields'),
    ]

    operations = [
        migrations.RunPython(migrate_to_deposition_fields),
    ]
