# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tasktracker_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'tasktracker', ['Tag'])

        # Adding M2M table for field tasks on 'Tag'
        m2m_table_name = db.shorten_name(u'tasktracker_tag_tasks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm[u'tasktracker.tag'], null=False)),
            ('task', models.ForeignKey(orm[u'tasktracker.task'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'task_id'])

        # Adding model 'Task'
        db.create_table(u'tasktracker_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_tasks', to=orm['tasktracker.User'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'tasktracker', ['Task'])

        # Adding M2M table for field assigned_to on 'Task'
        m2m_table_name = db.shorten_name(u'tasktracker_task_assigned_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'tasktracker.task'], null=False)),
            ('user', models.ForeignKey(orm[u'tasktracker.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'user_id'])

        # Adding model 'User'
        db.create_table(u'tasktracker_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('registration_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('pswd', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'tasktracker', ['User'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tasktracker_tag')

        # Removing M2M table for field tasks on 'Tag'
        db.delete_table(db.shorten_name(u'tasktracker_tag_tasks'))

        # Deleting model 'Task'
        db.delete_table(u'tasktracker_task')

        # Removing M2M table for field assigned_to on 'Task'
        db.delete_table(db.shorten_name(u'tasktracker_task_assigned_to'))

        # Deleting model 'User'
        db.delete_table(u'tasktracker_user')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tasktracker.user': {
            'Meta': {'ordering': "['login']", 'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'pswd': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['tasktracker']