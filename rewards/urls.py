
from django.conf.urls import include, url
from django.contrib import admin

from accounts import urls as accounts_urls
from classes import urls as classes_urls

urlpatterns = [
    url(r'^$', 'rewards.views.index', name = 'index'),
    url(r'^criar-pontuacao/$', 'rewards.views.create_reward', name = 'create_reward'),
    url(r'^criar-badge/$', 'rewards.views.create_badge', name = 'create_badge'),
]
