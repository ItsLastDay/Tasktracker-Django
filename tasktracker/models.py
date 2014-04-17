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
    date_fmt = 'Please use the following format: YYYY-MM-DD HH:MM' # I don't know actual one
    created_on = models.DateTimeField(help_text=date_fmt)
    assigned_to = models.ManyToManyField(User)
    expiration_date = models.DateTimeField(help_text=date_fmt)
    description = models.TextField()
    status = models.CharField(choices=[('cp', 'Closed'), ('op', 'Open')])

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        pass

class User(models.Model):
    login = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    registration_date = models.DateTimeField()
    pswd = models.CharField(max_length=255) # not sure in what form the hash will be

    def __unicode__(self):
        return self.login
    
    def get_absolute_url(self):
        pass
