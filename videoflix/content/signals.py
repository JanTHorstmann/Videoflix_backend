from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved!')
    if created:
        print('new Video created')

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, using, origin, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('File deleted:', instance.video_file.path)