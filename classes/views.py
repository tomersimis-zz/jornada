from django.shortcuts import render, redirect
from classes.forms import ClassForm
from classes.models import Class
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher
from django.core.urlresolvers import reverse
from rewards.models import Badge, Reward
from django.contrib import messages

import base64

from accounts.models import Teacher,Student

@login_required(login_url='/usuario/login/')
def index(request):

	teacher = is_teacher(request.user)

	if teacher:
		classes = Class.objects.filter(teachers__in=[Teacher.objects.get(user=request.user)])
	else:
		classes = Class.objects.filter(students__in=[Student.objects.get(user=request.user)])

	return render(request, 'classes/index.html', {
		'classes': classes,
		'classes_active': True,
		'is_teacher': teacher
	})

@login_required(login_url='/usuario/login/')
def remove(request, id):

	if not is_teacher(request.user):
		return redirect('index')

	if not Class.objects.filter(pk=id, teachers__in=[Teacher.objects.get(user=request.user)]):
		return redirect('index')

	Class.objects.get(pk=id).delete()

	return redirect('Classes:index')


@login_required(login_url='/usuario/login/')
def create_class(request):

	if not is_teacher(request.user):
		return redirect('index')

	class_form = ClassForm(request.POST or None)

	if class_form.is_valid():
		classe = class_form.save()
		classe.teachers.add(Teacher.objects.get(user=request.user))
		classe.save()
		return redirect('index')

	return render(request, 'classes/form.html', {
		'form': class_form,
		'edit': False
	})

@login_required(login_url='/usuario/login/')
def edit_class(request, id):

	if not is_teacher(request.user):
		return redirect('index')

	if not Class.objects.filter(pk=id, teachers__in=[Teacher.objects.get(user=request.user)]):
		return redirect('Classes:index')


	my_class = Class.objects.get(pk=id)
	class_form = ClassForm(request.POST or None, instance = my_class)

	if class_form.is_valid():
		my_class.save()
		return redirect('Classes:index')
		

	return render(request, 'classes/form.html', {
		'form': class_form,
		'edit': True
	})

@login_required(login_url='/usuario/login/')
def view(request, id):

	aux = set(Teacher.objects.all())
	aux2 = set(Class.objects.get(pk=id).teachers.all())

	aux -= aux2
			

	context={
		'class': Class.objects.get(pk=id),
		'key': base64.b64encode(bytes(id, 'utf-8')),
		'is_teacher': is_teacher(request.user),
		'teachers': aux

	}
	return render(request, 'classes/view_class.html', context)

@login_required(login_url='/usuario/login/')
def register(request, key):

	if is_teacher(request.user):
		return redirect('Classes:index')

	student_obj = Student.objects.get(user=request.user)

	pk = base64.b64decode(key)
	obj = Class.objects.get(pk=pk)

	if Class.objects.filter(pk=pk, students__in=[student_obj]):
		return redirect(reverse('Classes:view', kwargs={'id':pk}))

	# obj.students.add(student_obj)
	# obj.save()

	return render(request, 'classes/register.html', {
		'class': Class.objects.get(pk=pk),
		'key': key
	})

def confirm_register(request, key):
	if is_teacher(request.user):
		return redirect('Classes:index')

	student_obj = Student.objects.get(user=request.user)

	pk = base64.b64decode(key)
	obj = Class.objects.get(pk=pk)

	if Class.objects.filter(pk=pk, students__in=[student_obj]):
		return redirect(reverse('Classes:view', kwargs={'id':pk}))

	obj.students.add(student_obj)
	obj.save()

	return redirect('Classes:index')

def give_badges(request, id):

	obj = Class.objects.get(pk=id)
	badges = []
	for teacher in obj.teachers.all():
		badges = badges + list(Badge.objects.filter(created_by=teacher.user))

	if request.method == 'POST':
		badge = Badge.objects.get(pk=request.POST.get('badge'))
		students = Student.objects.filter(pk__in=request.POST.getlist('students[]'))
		for student in students:
			student.badges.add(badge)
			student.save()
		messages.success(request, 'Badges atribuídas com sucesso.')

	return render(request, 'classes/give_badges.html', {
		'class': obj,
		'badges': badges
	})

def atribuir_professor(request, id):

	if request.method == 'POST':
		prof = Teacher.objects.filter(pk__in=request.POST.getlist('teachers[]'))
		classe = Class.objects.get(pk=id)

		for teacher in prof:
			classe.teachers.add(teacher)
			classe.save()
		messages.success(request, 'Professor atribuído com sucesso.')

	return redirect(reverse('Classes:view', kwargs={'id':id}))

def give_rewards(request, id):

	obj = Class.objects.get(pk=id)
	rewards = []
	for teacher in obj.teachers.all():
		rewards = rewards + list(Reward.objects.filter(created_by=teacher.user))

	if request.method == 'POST':
		reward = Reward.objects.get(pk=request.POST.get('reward'))
		students = Student.objects.filter(pk__in=request.POST.getlist('students[]'))
		for student in students:
			student.rewards.add(reward)
			student.save()
		messages.success(request, 'Pontuações atribuídas com sucesso.')

	return render(request, 'classes/give_rewards.html', {
		'class': obj,
		'rewards': rewards
	})