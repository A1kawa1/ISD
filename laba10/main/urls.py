from django.contrib import admin
from django.urls import path, include
from main.views import main


app_name = 'main'
urlpatterns = [
    path('', main),
]
