from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jornada.util import is_teacher
from classes.models import Class
from accounts.models import Teacher, Student

@login_required(login_url='usuario/login/')
def index(request):
	context = {'index_active': True}

	if is_teacher(request.user):
		context['classes'] = Class.objects.filter(teachers__in=[Teacher.objects.get(user=request.user)])
	else:
		context['classes'] =  Class.objects.filter(students__in=[Student.objects.get(user=request.user)])

	return render(request, 'index.html', context)

def statistics(request):
	context = {'statistics_active': True}
	classes_context = []

	if is_teacher(request.user):
		classes = Class.objects.filter(teachers__in=[Teacher.objects.get(user=request.user)])
	else:
		classes = Class.objects.filter(students__in=[Student.objects.get(user=request.user)])

	for entry in classes:
			classes_context.append(entry)

	context['classes'] = classes_context
	
	return render(request, 'reports.html', context)
