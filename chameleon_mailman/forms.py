from __future__ import absolute_import
from django.forms import ModelForm
from .models import MailmanSubscription


class MailmanSubscriptionForm(ModelForm):

    class Meta:
        model = MailmanSubscription
        exclude = ['user']
