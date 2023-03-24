from django.urls import path
from graph.views import graph


urlpatterns = [
    path('', graph)
]
