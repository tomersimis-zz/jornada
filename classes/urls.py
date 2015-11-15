
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'classes.views.index', name = 'index'),
    url(r'^criar$', 'classes.views.create_class', name = 'create'),
    url(r'^editar/(?P<id>\d+)$', 'classes.views.edit_class', name= 'edit'),
    url(r'^remove/(?P<id>\d+)$', 'classes.views.remove', name = 'remove'),
    url(r'^registrar/(?P<key>.+)$', 'classes.views.register', name = 'register'),
    url(r'^badges/(?P<id>\d+)$', 'classes.views.give_badges', name = 'give_badges'),
    url(r'^pontuacao/(?P<id>\d+)$', 'classes.views.give_rewards', name = 'give_rewards'),
    url(r'^confirmar-registro/(?P<key>.+)$', 'classes.views.confirm_register', name = 'confirm_register'),
    url(r'^(?P<id>\d+)$', 'classes.views.view', name = 'view'),
]