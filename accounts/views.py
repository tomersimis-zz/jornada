from django.shortcuts import render, render_to_response, redirect
from accounts.forms import EditUserForm, TeacherForm, UserForm, StudentForm
from accounts.models import GRADE_CHOICES, Student, Teacher
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher
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
		'form': user_form,
		'teacher_form': teacher_form
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

	if request.user.is_authenticated():
		return redirect('index')

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

@login_required(login_url='/usuario/login/')
def edit(request):
	teacher = is_teacher(request.user)

	if teacher:
		custom_form = TeacherForm(request.POST or None, instance=Teacher.objects.get(user=request.user))
	else:
		custom_form = StudentForm(request.POST or None, instance=Student.objects.get(user=request.user))

	user_form = EditUserForm(request.POST or None, instance=request.user)

	if request.method == 'POST':
		if custom_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			custom_form.save()
			messages.success(request, 'Configurações editadas com sucesso')
	
	return render(request, 'accounts/edit.html', {
		'form': user_form,
		'custom_form': custom_form,
		'is_teacher': teacher
	}) 