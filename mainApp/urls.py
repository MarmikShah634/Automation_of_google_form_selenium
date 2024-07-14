from django.urls import include, path
from mainApp import views

urlpatterns = [
    path('', views.main, name='main'),
]