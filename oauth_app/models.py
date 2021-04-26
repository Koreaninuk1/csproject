from django.db import models

# Create your models here.
class Role(models.Model):
    email = models.EmailField()
    role = models.CharField(max_length=20)

class Appointments(models.Model):
    teacher = models.EmailField()
    student = models.EmailField()
    datetime = models.DateTimeField()

class AppointmentRequests(models.Model):
    teacher = models.EmailField()
    student = models.EmailField()
    datetime = models.DateTimeField()
