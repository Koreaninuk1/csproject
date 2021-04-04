from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    print(request.user)
    return render(request, 'index.html')

def login(request):
    return render(request, "accounts/login.html")