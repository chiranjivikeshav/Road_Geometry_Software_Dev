from django.shortcuts import render,redirect
from . import urls
# Create your views here.
def home(request):
    return render(request,'home.html')