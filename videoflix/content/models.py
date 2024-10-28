from django.db import models
import datetime
from django.conf import settings


class Video(models.Model):
    created_at = models.DateField(default=datetime.date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    category = models.CharField(max_length=80)
    thumbnail = models.FileField(upload_to='img', blank=True, null=True)

    def __str__(self):
        return self.title
    