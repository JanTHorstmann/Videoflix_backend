from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500, default='', blank=True)     
    phone = models.CharField(max_length=25, default='', blank=True)
    address = models.CharField(max_length=150, default='', blank=True) 
