from accounts.models import Teacher

def is_teacher(user):
	return Teacher.objects.filter(user=user).exists()