from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jornada.util import is_teacher
from rewards.forms  import RewardForm, BadgeForm
from rewards.models import Reward, Badge
from accounts.models import Teacher

# Create your views here.
@login_required(login_url='/usuario/login/')
def index(request):

	if not is_teacher(request.user):
		return redirect('index')

	return render(request, 'rewards/index.html', {
		'reward_form' : RewardForm(),
		'badge_form': BadgeForm(),
		'rewards' : Reward.objects.filter(created_by=request.user),
		'badges' : Badge.objects.filter(created_by=request.user),
	})


@login_required(login_url='/usuario/login/')
def create_reward(request):

	if not is_teacher(request.user):
		return redirect('index')

	reward_form = RewardForm(request.POST or None)

	if reward_form.is_valid():
		reward = reward_form.save(commit=False)
		reward.created_by = request.user
		reward.save()
		return redirect('index')

	return render(request, 'rewards/index.html', {
		'reward_form': reward_form,
		'badge_form' : BadgeForm(),
		'rewards' : Reward.object.filter(created_by=request.user),
		'badges' : Badge.object.filter(created_by=request.user),
	})


@login_required(login_url='/usuario/login/')
def create_badge(request):

	if not is_teacher(request.user):
		return redirect('index')

	badge_form = BadgeForm(request.POST or None)

	if badge_form.is_valid():
		badge = badge_form.save(commit=False)
		badge.created_by = request.user
		badge.save()
		#return redirect('index')

	print("COOOL")
	print(badge_form.errors)

	return render(request, 'rewards/index.html', {
		'badge_form': badge_form,
		'reward_form': RewardForm(),
		'rewards' : Reward.objects.filter(created_by=request.user),
		'badges' : Badge.objects.filter(created_by=request.user),
	})