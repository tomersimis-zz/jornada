from django.contrib import admin
from rewards.models import Reward, Badge, BadgeStudentClass, RewardStudentClass
from rewards.models import Badge
admin.site.register([Reward,Badge, BadgeStudentClass, RewardStudentClass])

# Register your models here.
