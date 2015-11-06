from django.db import models
from django.contrib.auth.models import User


class Info(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    dob = models.DateField(blank=True)
    bio = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    jabber = models.CharField(max_length=20, blank=True)
    skype = models.CharField(max_length=20, blank=True)
    other = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name
