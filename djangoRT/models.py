from __future__ import absolute_import
from django.db import models

class TicketCategories(models.Model):
    category_display_name = models.CharField(max_length=200, default="")
    category_field_name = models.CharField(max_length=200, default="")
