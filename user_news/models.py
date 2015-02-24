from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.contrib import messages
import re

class NewsTag(models.Model):
    tag = models.TextField(max_length=50)

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

"""
Super class for all news content
"""
class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    summary = RichTextField(max_length=600)
    body = RichTextField()
    tags = models.ManyToManyField(NewsTag, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def save(self):
        self.slug = slugify(self.title)
        super(News,self).save()

"""
Implementation for Events
"""
class Event(News):
    EVENT_TYPES = (
        ('CONFERENCE','Conference'),
        ('MEETING','Meeting'),
        ('PAPER','Paper'),
        ('POSTER','Poster'),
        ('PRESENTATION','Presentation'),
        ('TUTORIAL','Tutorial'),
        ('WORKSHOP','Workshop'),
        ('OTHER','Other'),
    )
    event_type = models.TextField(choices=EVENT_TYPES)
    event_date = models.DateTimeField('event date')

"""
Implementation for System Outages
"""
class Outage(News):
    start_date = models.DateTimeField('start of outage')
    end_date = models.DateTimeField('expected end of outage')

class OutageUpdate(News):
    original_item = models.ForeignKey(Outage)

"""
This class represents a notification which should be displayed to users using
the django.contrib.messages framework. Messages can be created and scheduled
for display.
"""
class Notification(models.Model):
    NOTIFICATION_LEVELS = (
        (messages.INFO, 'Informational'),
        (messages.SUCCESS, 'Success'),
        (messages.WARNING, 'Warning'),
        (messages.ERROR, 'Error'),
    )

    level = models.IntegerField(choices=NOTIFICATION_LEVELS)
    title = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    schedule_on = models.DateTimeField('scheduled display start', blank=True)
    schedule_off = models.DateTimeField('scheduled display end', blank=True)
    limit_pages = models.TextField('Limit display only to these page paths (one per line)', blank=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.message

    def display(self):
        return re.sub(r'\s+', ' ', u'<h4>{0}</h4>{1}'.format(self.title, self.message))