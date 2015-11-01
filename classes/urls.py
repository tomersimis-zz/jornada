
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^criar$', 'classes.views.create_class', name = 'create'),
]
