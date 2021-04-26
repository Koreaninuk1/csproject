from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from oauth_app.models import Role, Appointments, AppointmentRequests

def index(request):
    teachers = Role.objects.filter(role='teacher')
    context = {'teachers':[]}
    for teacher in teachers:
        if teacher.email != '' and teacher.email != request.user.email:
            context['teachers'].append(teacher.email)
    return render(request, 'index.html', context)

def get_calendar(request):
    if request.method == 'POST':
        appointments = Appointments.objects.filter(teacher=request.POST['teachers'])
        data = {'appointments':[]}
        for appointment in appointments:
            data['appointments'].append(appointment.datetime.strftime("%m/%d/%Y, %H:%M:%S"))
        return JsonResponse(data)
    else:
        return redirect('/')

def create_appointment(request):
    if request.method == 'POST':
        appointments = Appointments.objects.filter(teacher=request.POST['teacher'])
        already_appointed = False
        for appointment in appointments:
            if appointment.datetime.strftime("%Y-%m-%dT%H:%M") == request.POST['datetime']:
                already_appointed = True
                break
        if already_appointed:
            return HttpResponseBadRequest('That time is already appointed. Please select another time')
        else:
            AppointmentRequests(teacher=request.POST['teacher'], student=request.user.email, datetime=request.POST['datetime']).save()
            return HttpResponse('Appointment requested')
    else:
        return redirect('/')

def login(request):
    return render(request, "accounts/login.html")

def profile(request):
    if request.method == 'POST':
        role = request.POST['role']
        try:
            obj = Role.objects.filter(email=request.user.email)
            if len(obj) > 0:
                obj = obj[0]
                obj.role = role
                obj.save()
            else:
                Role(email=request.user.email, role=role).save()
        except Role.DoesNotExist:
            Role(email=request.user.email, role=role).save()
    obj = Role.objects.filter(email=request.user.email)
    context = {
        'role': 'student',
        'confirmed_appointments': [],
        'requested_appointments': [],
    }
    if len(obj) > 0:
        obj = obj[0]
        context['role'] = obj.role
    if context['role'] == 'student':
        confirmed_appointments = Appointments.objects.filter(student=request.user.email)
        for appointment in confirmed_appointments:
            context['confirmed_appointments'].append({'teacher': appointment.teacher, 'student': appointment.student, 'datetime': appointment.datetime.strftime("%m/%d/%Y, %H:%M:%S"), 'datetime_format_sync': appointment.datetime.strftime("%Y-%m-%d %H:%M:%S")})
        requested_appointments = AppointmentRequests.objects.filter(student=request.user.email)
        for appointment in requested_appointments:
            context['requested_appointments'].append({'teacher': appointment.teacher, 'student': appointment.student, 'datetime': appointment.datetime.strftime("%m/%d/%Y, %H:%M:%S"), 'datetime_format_sync': appointment.datetime.strftime("%Y-%m-%d %H:%M:%S")})
    else:
        confirmed_appointments = Appointments.objects.filter(teacher=request.user.email)
        for appointment in confirmed_appointments:
            context['confirmed_appointments'].append({'teacher': appointment.teacher, 'student': appointment.student, 'datetime': appointment.datetime.strftime("%m/%d/%Y, %H:%M:%S"), 'datetime_format_sync': appointment.datetime.strftime("%Y-%m-%d %H:%M:%S")})
        requested_appointments = AppointmentRequests.objects.filter(teacher=request.user.email)
        for appointment in requested_appointments:
            context['requested_appointments'].append({'teacher': appointment.teacher, 'student': appointment.student, 'datetime': appointment.datetime.strftime("%m/%d/%Y, %H:%M:%S"), 'datetime_format_sync': appointment.datetime.strftime("%Y-%m-%d %H:%M:%S")})
    return render(request, 'profile.html', context)

def cancel_appointment(request):
    if request.method == 'POST':
        teacher = request.POST['teacher']
        student = request.POST['student']
        datetime = request.POST['datetime']
        try:
            obj = Appointments.objects.filter(teacher=teacher, student=student, datetime=datetime)
            if len(obj) > 0:
                obj = obj[0]
                obj.delete()
                return redirect('/profile')
            else:
                return HttpResponseBadRequest('That appointment does not exist.')
        except Appointments.DoesNotExist:
            return HttpResponseBadRequest('That appointment does not exist.')
    else:
        return redirect('/profile')

def accept_appointment_request(request):
    if request.method == 'POST':
        teacher = request.POST['teacher']
        student = request.POST['student']
        datetime = request.POST['datetime']
        try:
            obj = AppointmentRequests.objects.filter(teacher=teacher, student=student, datetime=datetime)
            if len(obj) > 0:
                obj = obj[0]
                obj.delete()
                Appointments(teacher=teacher, student=student, datetime=datetime).save()
                return redirect('/profile')
            else:
                return HttpResponseBadRequest('That appointment request does not exist.')
        except Appointments.DoesNotExist:
            return HttpResponseBadRequest('That appointment request does not exist.')
    else:
        return redirect('/profile')

def decline_appointment_request(request):
    if request.method == 'POST':
        teacher = request.POST['teacher']
        student = request.POST['student']
        datetime = request.POST['datetime']
        try:
            obj = AppointmentRequests.objects.filter(teacher=teacher, student=student, datetime=datetime)
            if len(obj) > 0:
                obj = obj[0]
                obj.delete()
                return redirect('/profile')
            else:
                return HttpResponseBadRequest('That appointment request does not exist.')
        except Appointments.DoesNotExist:
            return HttpResponseBadRequest('That appointment request does not exist.')
    else:
        return redirect('/profile')
