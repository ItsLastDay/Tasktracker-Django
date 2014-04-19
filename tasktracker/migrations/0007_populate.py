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
            psw = gen_string(20)
            first_name = random.choice(names)
            last_name = random.choice(surnames)
            email = 'misha@koltsov.su'
            reg_date = gen_date()
            login = gen_string(7)
            users.append(orm.User(login=login, pswd=psw, first_name=first_name, last_name=last_name,\
                    email=email, registration_date=reg_date))
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
    symmetrical = True