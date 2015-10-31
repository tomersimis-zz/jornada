from django.forms import ModelForm
from django.contrib.auth.models import User
from accounts.models import Teacher, Student

class TeacherForm (ModelForm):

	class Meta:
		model = Teacher
		fields = ['school', 'disciplines']

class StudentForm(ModelForm):

	class Meta:
		model = Student
		fields = ['school', 'grade']

class UserForm(ModelForm):

	class Meta:
		model = User
		fields = ['username','first_name', 'last_name',\
		'email', 'password']