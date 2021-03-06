import os
from django.db import models
from PIL import Image


class Info(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    dob = models.DateField()
    bio = models.TextField(max_length=200)
    email = models.EmailField()
    jabber = models.CharField(max_length=20)
    skype = models.CharField(max_length=20)
    other = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='info', default='None')

    def save(self):
        previous_photo = self.photo.path
        super(Info, self).save()
        try:
            pw = self.photo.width
            ph = self.photo.height

            mw = 200
            mh = 200
            if pw > mw or ph > mh:
                    filename = str(self.photo.path)
                    image = Image.open(filename)
                    image.thumbnail((mw, mh), Image.ANTIALIAS)
                    image.save(filename)
            if previous_photo != self.photo.path:
                os.remove(previous_photo)
        except:
            return

    def __unicode__(self):
        return self.name


class WebRequest(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=20)
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    get = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    user = models.CharField(max_length=20, blank=True)
    priority = models.CharField(max_length=15, null=True, blank=True)

    def __unicode__(self):
        return self.host


class DatabaseLog(models.Model):
    model = models.CharField(max_length=20)
    action = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.model
