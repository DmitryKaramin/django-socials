from __future__ import unicode_literals

from django.db import models


class FacebookModel(models.Model):
    name = models.CharField(max_length=20, default='Facebook')
    email = models.EmailField(default=' ')
    client_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    client_secret = models.CharField(max_length=200, blank=True, null=True)
    user_access_token = models.CharField(max_length=500, blank=True, null=True)
    user_access = models.BooleanField(default=False)
    pages = models.ManyToManyField('Account', blank=True)

    def __unicode__(self):
        return self.email


class Account(models.Model):
    name = models.CharField(max_length=20, default=' ')
    page_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    page_access_token = models.CharField(max_length=500, blank=True, null=True)
    page_access = models.BooleanField(default=False)
    time_valid = models.CharField(max_length=50, blank=True, null=True)
    manage_pages_granted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
