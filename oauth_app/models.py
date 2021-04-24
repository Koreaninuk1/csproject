from django.db import models

# Create your models here.
class Role(models.Model):
    email = models.EmailField()
    role = models.CharField(max_length=20)
