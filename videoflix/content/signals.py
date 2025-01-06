from .models import Video
from content.tasks import convert_120p, convert_360p, convert_720p, convert_1080p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved!')
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_120p, instance.video_file.path)
        queue.enqueue(convert_360p, instance.video_file.path)
        queue.enqueue(convert_720p, instance.video_file.path)
        queue.enqueue(convert_1080p, instance.video_file.path)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, using, origin, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('Hauptvideo gelöscht:', instance.video_file.path)

            resolutions = ['_120p.mp4', '_360p.mp4', '_720p.mp4', '_1080p.mp4']
            for res in resolutions:
               res_file = instance.video_file.path[:-4] + res
               if os.path.isfile(res_file):
                os.remove(res_file)
                print(f'{res} gelöscht:', res_file)

    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
       os.remove(instance.thumbnail.path)
       print('Thumbnail gelöscht:', instance.thumbnail.path)
