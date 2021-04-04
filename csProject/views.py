from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    print(request.user)
    return render(request, 'index.html')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"