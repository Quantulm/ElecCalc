from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("calculator_home", views.calculator_home, name="calculator_home"),
    path(
        "calculator_base_selection",
        views.calculator_base_selection,
        name="calculator_base_selection",
    ),
    path(
        "calculator_option_selection",
        views.calculator_option_selection,
        name="calculator_option_selection",
    ),
    path(
        "calculator_result_selection",
        views.calculator_result_selection,
        name="calculator_result_selection",
    ),
    path("calculator_result", views.calculator_result, name="calculator_result"),
    path("download_data", views.download_data, name="download_data"),
    path("privacy", views.privacy, name="privacy"),
]
