from django.shortcuts import render, render_to_response, redirect
from accounts.forms import TeacherForm, UserForm

def signup_teacher(request):

	teacher_form = TeacherForm(request.POST or None)
	user_form = UserForm(request.POST or None)
	context = {}

	if request.method == 'POST':
		if teacher_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			teacher = teacher_form.save(commit = False)
			teacher.user = user
			teacher.save()
			return redirect('index_page')

	return render(request, 'signup_teacher.html', {
		'form': user_form
	})