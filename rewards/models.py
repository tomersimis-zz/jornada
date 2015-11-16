from django.db import models

from django.contrib.auth.models import User
from accounts.models import Student
from classes.models import Class

# Create your models here.
class Reward(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    value = models.IntegerField(blank=True, default = 0)
    created_by = models.ForeignKey(User)

    def __str__(self):
    	return self.name + " - Created by " + self.created_by.first_name


class Badge(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
    	return self.name + " - Created by " + self.created_by.first_name

class BadgeStudentClass(models.Model):
    badge = models.ForeignKey(Badge)
    student = models.ForeignKey(Student)
    classe = models.ForeignKey(Class)
    created = models.DateTimeField(auto_now_add=True)

class RewardStudentClass(models.Model):
    reward = models.ForeignKey(Reward)
    student = models.ForeignKey(Student)
    classe = models.ForeignKey(Class)
    created = models.DateTimeField(auto_now_add=True)