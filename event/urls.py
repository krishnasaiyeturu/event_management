from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# from django.urls import path

# Your path of views


urlpatterns = [

    url(r'^login', views.login),
    url(r'^logout/$', views.logout_view),

    url(r'^dashboard', views.index),

]