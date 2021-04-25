from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('lectureformat', views.lectureformat, name="calculator"),
]