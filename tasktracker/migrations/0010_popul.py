# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import random, string
from unidecode import unidecode

class Migration(DataMigration):
    def __populate(self, n_tasks, n_tags, n_users, orm):
        words = ['очень', 'важное', 'дело', 'проблема', 'срочно', 'отчётность', 'нужно', \
                'дать', 'ажиотаж', 'программа', 'куча', 'страниц']
        names = ['Петя', 'Маша', 'Измаил', 'Миша', 'Костя', 'Егор', 'Геннадий']
        surnames = ['Иванов', 'Петров', 'Сидоров', 'Разумейский', 'Хорнилов', 'Мамонов']
        a = ['а', 'е', 'и', 'о', 'у']
        b = ['к', 'н', 'р', 'й', 'м', 'б', 'ж', 'ш', 'ф', 'ч', 'х', 'з', 'п', 'р', 'л', 'в', 'д', 'ц']
        decoder = lambda x: unidecode(x.decode('utf-8'))
        words = map(decoder, words)
        names = map(decoder, names)
        surnames = map(decoder, surnames)
        bigrams = []
        for x in a:
            for y in b:
                bigrams.append(y + x)
        bigrams = map(decoder, bigrams)
        def gen_string(n):
            return ''.join([random.choice(string.letters) for i in range(n)])
        def gen_date():
            res = ''
            res += str(random.randint(1990, 2010)) + '-'
            res += str(random.randint(1, 12)) + '-'
            res += str(random.randint(1, 25)) + ' '
            tm = str(random.randint(0, 23)) + ':'
            if len(tm) < 3:
                tm = '0' + tm
            mm = str(random.randint(0, 59))
            if len(mm) < 2:
                mm = '0' + mm
            tm += mm
            res += tm
            return res

        # populate tags
        titles = []
        for _ in range(n_tags):
            length = random.randint(3, 8)
            title = ''.join([random.choice(bigrams) for i in range(length)])
            titles.append(title)
        titles = list(set(titles))
        tags = []
        for title in titles:
            tag = orm.Tag(title=title)
            tags.append(tag)
            tag.save()

        # populate users
        users = []
        for _ in range(n_users):
            psw = '1234'
            first_name = random.choice(names)
            last_name = random.choice(surnames)
            email = 'misha@koltsov.su'
            reg_date = gen_date()
            login = gen_string(7)
            users.append(orm.User(username=login, password=psw, first_name=first_name, last_name=last_name,\
                    email=email, registration_date=reg_date))
            users.set_password(psw)
        for user in users:
            user.save()

        #populate tasks
        tasks = []
        for _ in range(n_tasks):
            title = ' '.join([random.choice(words) for i in range(7)]).capitalize() 
            rating = random.randint(1, 10)
            created_on = gen_date()
            expiration_date = gen_date() if random.randint(1, 2) == 2 else None
            description = ' '.join([random.choice(bigrams) for i in range(20)])
            status = 'op' if random.randint(1, 2) == 2 else 'cp'
            created_by = random.choice(users)
            assigned_to = [random.choice(users) for i in range(random.randint(1, 5))]
            tasks.append(orm.Task(title=title, rating=rating, created_on=created_on,\
                    expiration_date=expiration_date, description=description, status=status,\
                    created_by=created_by))
            tasks[-1].save()
            for man in assigned_to:
                tasks[-1].assigned_to.add(man)
        for task in tasks:
            task.save()

        # add tags for random tasks
        for tag in tags:
            for i in range(4):
                t = random.choice(tasks)
                tag.tasks.add(t)
            tag.save()
            
            
    def forwards(self, orm):
        "Write your forwards methods here."
        self.__populate(500, 100, 1000, orm)
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tasktracker.tag': {
            'Meta': {'ordering': "['title']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tasktracker.Task']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'tasktracker.task': {
            'Meta': {'ordering': "['pk', '-created_on']", 'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_tasks'", 'symmetrical': 'False', 'to': u"orm['tasktracker.User']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tasks'", 'to': u"orm['tasktracker.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tasktracker.user': {
            'Meta': {'ordering': "['username']", 'object_name': 'User', '_ormbases': [u'auth.User']},
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tasktracker']
    symmetrical = True
