from django.db import models

class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset()

    def open(self):
        # 1: all tasks with status = open
        return self.filter(status='op')

    def closed(self):
        # 2: all tasks with status = closed
        return self.filter(status='cp')

    def infinite(self):
        # 3: all tasks with no expiration date
        return self.filter(expiration_date__isnull=True)

    def query1(self):
        # 4: all tasks with rating > 4 and assigned to > 2 users
        return self.filter(rating__gt=4).annotate(num_assigned=models.Count('assigned_to')).filter(num_assigned__gt=2)

class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField('Task')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Task(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey('User', related_name='created_tasks')
    rating = models.IntegerField(db_index=True)
    date_fmt = 'Please use the following format: YYYY-MM-DD HH:MM' # I don't know actual one
    created_on = models.DateTimeField(help_text=date_fmt, db_index=True)
    assigned_to = models.ManyToManyField('User', related_name='assigned_tasks')
    expiration_date = models.DateTimeField(help_text=date_fmt, db_index=True, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=4, choices=[('cp', 'Closed'), ('op', 'Open')])
    objects = TaskManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        pass

    class Meta:
        ordering = ['-created_on']

class User(models.Model):
    login = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    registration_date = models.DateTimeField(db_index=True)
    pswd = models.CharField(max_length=255) # not sure in what form the hash will be

    def __unicode__(self):
        return self.login
    
    def get_absolute_url(self):
        pass

    class Meta:
        ordering = ['login']


