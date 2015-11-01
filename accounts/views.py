from django.shortcuts import render, render_to_response, redirect
from accounts.forms import TeacherForm, UserForm, StudentForm
from accounts.models import GRADE_CHOICES
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def signup_teacher(request):

	teacher_form = TeacherForm(request.POST or None)
	user_form = UserForm(request.POST or None)

	if request.method == 'POST':
		if teacher_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			teacher = teacher_form.save(commit = False)
			teacher.user = user
			teacher.save()
			return redirect('index')

	return render(request, 'signup_teacher.html', {
		'form': user_form
	})

def signup_student(request):

	student_form = StudentForm(request.POST or None)
	user_form = UserForm(request.POST or None)

	if request.method == 'POST':
		if student_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			student = student_form.save(commit = False)
			student.user = user
			student.save()
			return redirect('index')
	
	return render(request, 'signup_student.html', {
		'form': user_form,
		'student_form': student_form,
		'grades': GRADE_CHOICES,
	})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return redirect('index')
			else:
				messages.error(request, 'Problemas na autenticação do usuário')
		else:
			messages.error(request, 'Dados de usuário inválidos. Por favor, tente novamente.')

	return render(request, 'login.html')