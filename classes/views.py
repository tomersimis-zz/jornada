from django.shortcuts import render
from classes.forms import ClassForm
from classes.models import GRADE_CHOICES

# Create your views here.
def create_class(request):
    class_form = ClassForm(request.POST or None)

    if request.method == 'POST':
        if class_form.is_valid():
            classe = class_form.save()
            return redirect('index_page')

    return render(request, 'create_class.html', {'form': class_form, 'grades': GRADE_CHOICES})
