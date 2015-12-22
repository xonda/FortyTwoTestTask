from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import DatabaseLog


EXCLUDE_SIGNALS = ['WebRequest', 'DatabaseLog', 'LogEntry']


@receiver(post_save, dispatch_uid='RanDomDom')
def object_update(sender, **kwargs):
    obj_model = kwargs.get('instance').__class__.__name__
    if obj_model in EXCLUDE_SIGNALS:
        return
    created = kwargs.get('created')
    action = 'create' if created else 'edit'
    DatabaseLog.objects.create(model=obj_model, action=action)


@receiver(post_delete, dispatch_uid='DooWop')
def object_post_delete(sender, **kwargs):
    obj_model = kwargs.get('instance').__class__.__name__
    if obj_model in EXCLUDE_SIGNALS:
        return
    DatabaseLog.objects.create(model=obj_model, action='delete')
