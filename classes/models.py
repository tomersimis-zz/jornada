from django.db import models

from accounts.models import Teacher, Student, GRADE_CHOICES

# Create your models here.
class Class(models.Model):
	teachers = models.ManyToManyField(Teacher)
	name = models.CharField(max_length=50, blank=True)
	grade = models.CharField(max_length=50, blank=True, choices=GRADE_CHOICES)
	discipline = models.CharField(max_length=50, blank=True)
	time = models.TimeField(blank=True)
	location = models.CharField(max_length=100, blank=True)
	students = models.ManyToManyField(Student)
	description = models.CharField(max_length=200, blank=True)