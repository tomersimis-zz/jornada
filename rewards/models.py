from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Reward(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    value = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
    	return self.name + " - Created by " + self.created_by.first_name


class Badge(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
    	return self.name + " - Created by " + self.created_by.first_name