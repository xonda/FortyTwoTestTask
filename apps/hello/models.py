from PIL import Image
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Info(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    dob = models.DateField(blank=True)
    bio = models.TextField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    jabber = models.CharField(max_length=20, blank=True)
    skype = models.CharField(max_length=20, blank=True)
    other = models.TextField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='info', default='default_image.jpg')

    def save(self):
        super(Info, self).save()
        pw = self.photo.width
        ph = self.photo.height

        mw = 200
        mh = 200
        if pw > mw or ph > mh:
            try:
                filename = str(self.photo.path)
                image = Image.open(filename)
                image.thumbnail((mw, mh), Image.ANTIALIAS)
                image.save(filename)
            except IOError:
                print 'oops'

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

    def __unicode__(self):
        return self.host


class DatabaseLog(models.Model):
    model = models.CharField(max_length=20)
    action = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.model


EXCLUDE_SIGNALS = ['WebRequest', 'DatabaseLog', 'LogEntry']


@receiver(post_save, dispatch_uid='RanDomDom')
def object_update(sender, **kwargs):
    obj_model = kwargs.get('instance').__class__.__name__
    if obj_model in EXCLUDE_SIGNALS:
        return
    if not kwargs.get('created'):
        DatabaseLog.objects.create(model=obj_model, action='edit')
    else:
        DatabaseLog.objects.create(model=obj_model, action='create')


@receiver(post_delete, dispatch_uid='DooWop')
def object_post_delete(sender, **kwargs):
    obj_model = kwargs.get('instance').__class__.__name__
    if obj_model in EXCLUDE_SIGNALS:
        return
    DatabaseLog.objects.create(model=obj_model, action='delete')
