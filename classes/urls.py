
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'classes.views.index', name = 'index'),
    url(r'^criar$', 'classes.views.create_class', name = 'create'),
    url(r'^editar/(?P<id>\d+)$', 'classes.views.edit_class', name= 'edit'),
    url(r'^remove/(?P<id>\d+)$', 'classes.views.remove', name = 'remove'),
    url(r'^/(?P<id>\d+)$', 'classes.views.view', name = 'view'),
]