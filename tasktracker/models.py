from django.db import models
from django.contrib import auth

class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset()

    def open(self):
        # 1: all tasks with status = open
        return self.filter(status=Task.OPEN)

    def closed(self):
        # 2: all tasks with status = closed
        return self.filter(status=Task.CLOSED)

    def infinite(self):
        # 3: all tasks with no expiration date
        return self.filter(expiration_date__isnull=True)

    def query1(self, r_thresh=4, assigned_thresh=2):
        # 4: all tasks with rating > 4 and assigned to > 2 users
        return self.filter(rating__gt=r_thresh).annotate(num_assigned=models.Count('assigned_to')).filter(num_assigned__gt=assigned_thresh)

    def query_tags(self, tags_thresh=3):
        # 5: all tasks with more than 3 tags
        return self.annotate(num_tags=models.Count('tag')).filter(num_tags__gt=tags_thresh)

    def get_popular(self, start=0, top=10):
        # 6: popular tasks, with offset
        return self.order_by('rating').reverse()[start:start+top]

    def valid(self):
        # 7: tasks with valid date (expiration >= creation) or with no expiration date
        q = models.Q(created_on__lt=models.F('expiration_date'))
        q |= models.Q(expiration_date__isnull=True)
        return self.filter(q)

class UserManager(models.Manager):
    def get_newest(self, start=0, top=10):
        return self.order_by('registration_date').reverse()[start:start+top]

class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField('Task')
    
    def refers_to_task_with_a_lot_of_users(self, assigned_thresh=4):
        return self.tasks.annotate(num_assigned=models.Count('assigned_to')).aggregate(models.Max('num_assigned'))["num_assigned__max"] >\
                assigned_thresh

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Task(models.Model):
    CLOSED = 'cp'
    OPEN = 'op'
    STATUS_CHOICES = (
            (CLOSED, 'Closed'),
            (OPEN, 'Open')
        )
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey('User', related_name='created_tasks')
    rating = models.IntegerField(db_index=True)
    date_fmt = 'Please use the following format: YYYY-MM-DD HH:MM' 
    created_on = models.DateTimeField(help_text=date_fmt, db_index=True)
    assigned_to = models.ManyToManyField('User', related_name='assigned_tasks')
    expiration_date = models.DateTimeField(help_text=date_fmt, db_index=True, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=4, db_index=True, choices=STATUS_CHOICES)
    objects = TaskManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return 'tasks/%d' % self.id

    class Meta:
        ordering = ['-created_on']

class User(auth.models.User):
    registration_date = models.DateTimeField(db_index=True)
    objects = UserManager()

    def email_domain(self):
        return self.email[self.email.index('@') + 1:]

    def __unicode__(self):
        return self.username
    
    def get_absolute_url(self):
        return '/users/' + self.username

    class Meta:
        ordering = ['username']


