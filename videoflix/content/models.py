from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

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


class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progress')
    played_time = models.FloatField(help_text='Time played in seconds')
    duration = models.FloatField(help_text='Time played in seconds')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} - {self.video} - {self.played_time}s"