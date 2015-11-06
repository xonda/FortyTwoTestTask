# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WebRequest'
        db.delete_table(u'hello_webrequest')


    def backwards(self, orm):
        # Adding model 'WebRequest'
        db.create_table(u'hello_webrequest', (
            ('cookies', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('get', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('is_secure', self.gf('django.db.models.fields.BooleanField')()),
            ('post', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('is_ajax', self.gf('django.db.models.fields.BooleanField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hello', ['WebRequest'])


    models = {
        u'hello.info': {
            'Meta': {'object_name': 'Info'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['hello']