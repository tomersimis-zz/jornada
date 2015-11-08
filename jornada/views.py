from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from jornada.util import is_teacher
from classes.models import Class
from accounts.models import Teacher, Student

@login_required(login_url='usuario/login/')
def index(request):

	context = {}

	if is_teacher(request.user):
		context['classes'] = Class.objects.filter(teachers__in=[Teacher.objects.get(user=request.user)])
	else:
		context['classes'] =  Class.objects.filter(students__in=[Student.objects.get(user=request.user)])

	return render(request, 'index.html', context)