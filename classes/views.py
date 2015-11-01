from django.shortcuts import render, redirect
from classes.forms import ClassForm
from classes.models import GRADE_CHOICES
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher

from accounts.models import Teacher


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
