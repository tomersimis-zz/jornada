from django.shortcuts import render, redirect
from classes.forms import ClassForm
from classes.models import Class
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher

from accounts.models import Teacher

@login_required(login_url='/usuario/login/')
def index(request):

	if is_teacher(request.user):

		classes = Class.objects.filter(teachers__in=[Teacher.objects.get(user=request.user)])
	else:
		classes = []

	return render(request, 'classes/index.html', {
		'classes': classes
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
		'form': class_form
	})
