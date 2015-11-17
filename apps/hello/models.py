from django.db import models


class Info(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    dob = models.DateField(blank=True)
    bio = models.TextField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    jabber = models.CharField(max_length=20, blank=True)
    skype = models.CharField(max_length=20, blank=True)
    other = models.TextField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name
