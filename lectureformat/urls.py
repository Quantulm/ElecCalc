from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('calculator', views.calculator, name="calculator"),
    path('lectureformat', views.lectureformat, name="lectureformat"),
    path('toymodel', views.toymodel, name="toymodel")
]