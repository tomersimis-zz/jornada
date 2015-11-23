from django.shortcuts import render, redirect
from classes.forms import ClassForm
from classes.models import Class
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher
from django.core.urlresolvers import reverse
from rewards.models import Badge, Reward, BadgeStudentClass, RewardStudentClass
from django.contrib import messages

from datetime import datetime, date

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
		return redirect('Classes:index')

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

	obj = Class.objects.get(pk=id)

	aux = set(Teacher.objects.all())
	aux2 = set(obj.teachers.all())

	aux -= aux2
	
	students = obj.students.all()

	for student in students:
		rewards = RewardStudentClass.objects.filter(student=student, classe=obj)
		student.score = 0
		for reward in rewards:
			student.score += reward.reward.value

	students = list(students)

	students.sort(key=lambda x: x.score, reverse=True)

	rewards = RewardStudentClass.objects.filter(classe=obj)
	ranking_rewards = {}
	for s in students:
		for r in rewards:
			count = RewardStudentClass.objects.filter(classe=obj, student=s).count()
			if not r.reward.pk in ranking_rewards or ranking_rewards[r.reward.pk]['count'] < count:
				ranking_rewards[r.reward.pk] = {
					'count': count,
					'reward': r.reward,
					'student': s
				} 

	ranking_rewards = [ranking_rewards[r] for r in ranking_rewards]

	context={
		'class': obj,
		'key': base64.b64encode(bytes(id, 'utf-8')),
		'is_teacher': is_teacher(request.user),
		'teachers': aux,
		'students': students,
		'ranking_rewards': ranking_rewards

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
			bsc = BadgeStudentClass()
			bsc.student = student
			bsc.badge = badge
			bsc.classe = obj
			bsc.save()
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
			bsc = RewardStudentClass()
			bsc.student = student
			bsc.reward = reward
			bsc.classe = obj
			bsc.save()
		messages.success(request, 'Pontuações atribuídas com sucesso.')

	return render(request, 'classes/give_rewards.html', {
		'class': obj,
		'rewards': rewards
	})

@login_required(login_url='/usuario/login/')
def stats(request, id):

	obj = Class.objects.get(pk=id)

	students = obj.students.all()

	selected = False

	if request.GET.get('start') and request.GET.get('end'):
		selected = True

		initial_date = datetime.strptime('01/01/2000', '%d/%m/%Y')
		start_date = datetime.strptime(request.GET.get('start') + ' 00:00', '%d/%m/%Y %H:%M')
		end_date = datetime.strptime(request.GET.get('end') + ' 23:59', '%d/%m/%Y %H:%M')

		for student in students:
			initial_rewards = RewardStudentClass.objects.filter(student=student, classe=obj, created__range=(initial_date, start_date))
			student.initial_score = 0
			for r in initial_rewards:
				student.initial_score += r.reward.value

			rewards = RewardStudentClass.objects.filter(student=student, classe=obj, created__range=(start_date, end_date))
			student.score = 0
			for r in rewards:
				student.score += r.reward.value
			
			if student.score < student.initial_score:
				student.score_raise = -((student.initial_score or 1)/(student.score or 1))*100
			else:
				student.score_raise = (student.score/(student.initial_score or 1))*100

			student.badges = BadgeStudentClass.objects.filter(student=student, classe=obj, created__range=(start_date, end_date))

	context={
		'class': obj,
		'is_teacher': is_teacher(request.user),
		'students': students,
		'selected': selected
	}
	return render(request, 'classes/stats.html', context)
