from django.urls import path
from mainApp import views

urlpatterns = [
    path('', views.main, name='main'),
]