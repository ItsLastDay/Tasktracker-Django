#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
    from tasktracker.models import *

    print '# 1: all tasks with status = open'
    print Task.objects.open().values('pk', 'status')
    print '\n\n'
    print '# 2: all tasks with status = closed'
    print Task.objects.closed().values('pk', 'status')
    print '\n\n'
    print '# 3: all tasks with no expiration date'
    print Task.objects.infinite().values('pk', 'expiration_date')
    print '\n\n'
    print '# 4: all tasks with rating > 4 and assigned to > 2 users'
    print Task.objects.query1().values('num_assigned', 'rating', 'pk')
    print '\n\n'
    print '# 5: all tasks with more than 3 tags' 
    print Task.objects.query_tags().values('pk', 'num_tags')
    print '\n\n'
    print '# 6: popular tasks, top 10 from 60th place'
    print Task.objects.get_popular(start=60, top=10).values('pk', 'rating')
    print '\n\n'
    print '# 7: tasks with valid date (expiration >= creation) or with no expiration date'
    print Task.objects.valid().values('pk', 'created_on', 'expiration_date')
    print '\n\n'
    print '# 8: tags, for which there exists a task with that tag, that is assigned to >= 4 users'
    print filter(Tag.refers_to_task_with_a_lot_of_users, Tag.objects.all())
    print '\n\n'
    print '# 9: unique user email domains'
    print set([user.email_domain() for user in User.objects.all()])
    print '\n\n'
    print '# 10: top 10 newest users'
    print User.objects.get_newest().values('login', 'registration_date')
