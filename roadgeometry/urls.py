from django.contrib import admin
from django.urls import path
from roadgeometry import views

urlpatterns = [
    path('',views.home,name='home'),
]