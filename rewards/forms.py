from django.forms import ModelForm
from django.contrib.auth.models import User
from rewards.models import Badge, Reward

class RewardForm (ModelForm):

	class Meta:
		model = Reward
		fields = ['name', 'description', 'value', 'associated_class']

class BadgeForm (ModelForm):

	class Meta:
		model = Badge
		fields = ['name', 'description', 'associated_class']