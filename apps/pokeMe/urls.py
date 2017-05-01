from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^pokes$', views.homepage),
    url(r'^poking/(?P<user_id>\d+)$', views.poking),
    url(r'^logout$', views.logout),
]
