from django.db import models

from accounts.models import Teacher, Student, GRADE_CHOICES

# Create your models here.

GRADE_CHOICES = (
	('1ef', '1º ano'),
	('2ef', '2º ano'),
	('3ef', '3º ano'),
	('4ef', '4º ano'),
	('5ef', '5º ano'),
	('6ef', '6º ano'),
	('7ef', '7º ano'),
	('8ef', '8º ano'),
	('9ef', '9º ano'),
	('1em', '1º ano EM'),
	('2em', '2º ano EM'),
	('3em', '3º ano EM'),
)

class Class(models.Model):
	teachers = models.ManyToManyField(Teacher)
	name = models.CharField(max_length=50, blank=True)
	grade = models.CharField(max_length=50, blank=True, choices=GRADE_CHOICES)
	discipline = models.CharField(max_length=50, blank=True)
	time = models.TimeField(blank=True, null=True)
	location = models.CharField(max_length=100, blank=True)
	students = models.ManyToManyField(Student)
	description = models.CharField(max_length=200, blank=True)

	def students_ordered_by_rank(self):
		return self.students.all().annotate(rewards_sum = models.Sum("rewards__value")).order_by("-rewards_sum")

	def __str__(self):
	   return self.name + " - " + self.teachers.all()[0].user.first_name
