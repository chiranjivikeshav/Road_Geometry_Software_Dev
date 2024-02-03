from django.contrib import admin
from django.urls import path
from roadgeometry import views
from .views import save_coordinates

urlpatterns = [
    path('',views.home,name='home'),
    path('api/save-coordinates/', save_coordinates, name='save_coordinates'),
]

