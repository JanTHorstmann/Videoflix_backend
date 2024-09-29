from django.db import models
import datetime

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(default=datetime.date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)

    def __str__(self):
        return self.title
    