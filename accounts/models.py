from django.db import models

from django.contrib.auth.models import User

from rewards.models import Badge, Reward

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

class Teacher(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='images/users')
    school = models.CharField(max_length=100, blank=True)
    disciplines = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Student(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='images/users')
    school = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=50, blank=True, choices=GRADE_CHOICES)
    badges = models.ManyToManyField(Badge)
    rewards = models.ManyToManyField(Reward)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

# class Admin(models.Model):
#   user = models.OneToOneField(User)
#   access = models.CharField(max_length=200, blank=True)