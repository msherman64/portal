import json
import re

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from sharing_portal.utils import get_zenodo_file_link
from sharing_portal.conf import JUPYTERHUB_URL, ZENODO_SANDBOX
from sharing_portal.zenodo import ZenodoClient


def validate_git_repo(repo):
    """Validator to make sure that the GitHub repo is in the right format

    Args:
        repo (str): GitHub repo reference to validate.

    Raises:
        ValidationError: if the Git repo reference is not of the form
            {user|org}/{repo}
    """
    if not re.match(r"[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+", str(repo)):
        raise ValidationError("This must be in the form {user|org}/{repo}")


def validate_zenodo_doi(doi):
    """Validator to make sure that the Zenodo DOI is in the right format

    Args:
        doi (str): the Zenodo DOI to validate.

    Raises:
        ValidationError: if the DOI is malformed
    """
    if not re.match(r'10\.[0-9]+\/zenodo\.[0-9]+$', str(doi)):
        raise ValidationError("Please enter a valid Zenodo DOI")


class Author(models.Model):
    """
    Represents authors of an artifact
    """
    affiliation = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)

    # Order by last name
    class Meta:
        ordering = ('name',)

    def __str__(self):
        display = self.name
        if self.affiliation:
            display += ' ({})'.format(self.affiliation)
        return display


class LabelField(models.CharField):
    """ Custom field that is always lowercase """
    def to_python(self, value):
        return value.lower()


class Label(models.Model):
    """
    Represents artifact tags
    """
    label = LabelField(max_length=50)

    class Meta:
        ordering = ('label',)

    def __str__(self):
        return self.label


class Artifact(models.Model):
    """
    Represents artifacts
    These could be research projects, Zenodo depositions, etc
    """
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='artifacts')
    short_description = models.CharField(max_length=70, blank=True, null=True)
    description = models.TextField(max_length=5000)
    doi = models.CharField(max_length=50, blank=True, null=True,
                           validators=[validate_zenodo_doi])
    git_repo = models.CharField(max_length=200, blank=True,
                                null=True, validators=[validate_git_repo])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='artifacts',
                                   null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    labels = models.ManyToManyField(Label, related_name='artifacts',
                                    blank=True)
    associated_artifacts = models.ManyToManyField('Artifact',
                                                  related_name='associated',
                                                  blank=True)
    launch_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title

    @property
    def versions(self):
        return self.artifact_versions.order_by('created_at')

    @property
    def related_items(self):
        """Find related artifacts based on labels.

        FIXME: this method looks to use an expensive query to get all the related
        items from the database. It could likely be simplified into a more efficient
        query with some QuerySet wrangling. Could also not really be a problem
        depending on how it executes under the hood.
        """
        related_list = [
            artifact
            for label in self.labels.all()
            for artifact in label.artifacts.all()
            if artifact.id != self.id
        ]
        related_list = list(set(related_list))
        return related_list[:6]

    @property
    def search_terms(self):
        terms = self.title.lower().split()
        terms.extend([l.label.lower() for l in self.labels.all()])
        return terms


class ArtifactVersion(models.Model):
    ZENODO = 'zenodo'
    CHAMELEON = 'chameleon'
    GIT = 'git'
    DEPOSITION_REPO_CHOICES = (
        (ZENODO, 'Zenodo'),
        (CHAMELEON, 'Chameleon'),
        (GIT, 'Git'),
    )

    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='artifact_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    deposition_id = models.CharField(max_length=50)
    deposition_repo = models.CharField(max_length=24, choices=DEPOSITION_REPO_CHOICES, default=CHAMELEON)
    launch_count = models.IntegerField(default=0)

    def clean(self):
        if self.deposition_repo == self.ZENODO:
            validate_zenodo_doi(self.deposition_id)
        elif self.deposition_repo == self.GIT:
            validate_git_repo(self.deposition_id)

    @property
    def doi(self):
        if self.deposition_repo == self.ZENODO:
            return self.deposition_id
        else:
            return None

    @property
    def deposition_url(self):
        if self.deposition_repo == self.ZENODO:
            if ZENODO_SANDBOX:
                base_url = 'https://sandbox.zenodo.org'
            else:
                base_url = 'https://zenodo.org'
            return '{}/record/{}'.format(base_url, ZenodoClient.to_record(self.doi))
        else:
            return None

    @property
    def launch_url(self):
        base_url = JUPYTERHUB_URL + '/hub/import'
        query = dict(
            source=self.deposition_repo,
            id=self.deposition_id,
        )
        return base_url + '?' + urlencode(query)
