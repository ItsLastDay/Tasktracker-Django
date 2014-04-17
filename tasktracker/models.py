from django.db import models

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField(Task)

    def __unicode__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
    rating = models.IntegerField()
    date_fmt = 'Please use the following format: YYYY-MM-DD 12:25' # I don't know actual one
    created_on = models.DateTimeField(help_text=date_fmt)
    assigned_to = models.ManyToManyField(User)
    expiration_date = models.DateTimeField(help_text=date_fmt)
    description = models.TextField()
    status = models.CharField(choices=[('cp', 'Closed'), ('op', 'Open')])

    def __unicode__(self):
        return self.title

class User(models.Model):
    login = models.CharField(unique=True, editable=False)
    
    def __unicode__(self):
        return self.login

