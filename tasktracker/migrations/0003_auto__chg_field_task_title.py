# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.title'
        db.alter_column(u'tasktracker_task', 'title', self.gf('django.db.models.fields.CharField')(max_length=254))

    def backwards(self, orm):

        # Changing field 'Task.title'
        db.alter_column(u'tasktracker_task', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'tasktracker.tag': {
            'Meta': {'ordering': "['title']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tasktracker.Task']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'tasktracker.task': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_tasks'", 'symmetrical': 'False', 'to': u"orm['tasktracker.User']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tasks'", 'to': u"orm['tasktracker.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'tasktracker.user': {
            'Meta': {'ordering': "['login']", 'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'pswd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['tasktracker']