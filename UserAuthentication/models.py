from django.db import models

# Create your models here.

class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)

from db_connection import db

# Create your models here.

user_trial_collection = db['user_trial']