from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    label = models.CharField(max_length=200)
    hostname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=200)
    command = models.CharField(max_length=300)
    owner = models.ForeignKey(User)
    cwd = models.CharField(max_length=200)
    def __unicode__(self):
        return self.label
