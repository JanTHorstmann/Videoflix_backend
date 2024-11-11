from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    custom = models.CharField(max_length=500, default='', blank=True)     
    phone = models.CharField(max_length=25, default='', blank=True)
    address = models.CharField(max_length=150, default='', blank=True) 
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=20, blank=True, null=True)
    reset_token = models.CharField(max_length=50, blank=True, null=True)
    reset_token_expires = models.DateTimeField(blank=True, null=True)

    def set_reset_token(self):
        """Generiere einen neuen Reset-Token und speichere das Ablaufdatum."""
        self.reset_token = get_random_string(20)
        print(self.reset_token)
        self.reset_token_expires = timezone.now() + timedelta(hours=24)
        self.save()
