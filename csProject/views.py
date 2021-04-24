from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from oauth_app.models import Role

def index(request):
    print(request.user)
    return render(request, 'index.html')

def login(request):
    return render(request, "accounts/login.html")

def profile(request):
    if request.method == 'POST':
        role = request.POST['role']
        try:
            obj = Role.objects.filter(email=request.user.email)[0]
            print(obj.role)
            obj.role = role
            print(obj.role)
            obj.save()
        except Role.DoesNotExist:
            Role(email=request.user.email, role=role).save()
    obj = Role.objects.filter(email=request.user.email)[0]
    context = {}
    context['role'] = obj.role
    return render(request, 'profile.html', context)
