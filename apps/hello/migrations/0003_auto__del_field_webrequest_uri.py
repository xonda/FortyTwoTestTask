# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WebRequest.uri'
        db.delete_column(u'hello_webrequest', 'uri')


    def backwards(self, orm):
        # Adding field 'WebRequest.uri'
        db.add_column(u'hello_webrequest', 'uri',
                      self.gf('django.db.models.fields.CharField')(default='/', max_length=2000),
                      keep_default=False)


    models = {
        u'hello.info': {
            'Meta': {'object_name': 'Info'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'other': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'hello.webrequest': {
            'Meta': {'object_name': 'WebRequest'},
            'get': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ajax': ('django.db.models.fields.BooleanField', [], {}),
            'is_secure': ('django.db.models.fields.BooleanField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']