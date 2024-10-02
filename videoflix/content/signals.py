from .models import Video
from content.tasks import convert_480p, convert_720p, convert_1080p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

# ffmpeg -i "SOURCE_PATH" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "TARGET_PATH"
# ffmpeg -i "SOURCE_PATH" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "TARGET_PATH"

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved!')
    if created:
        convert_480p(instance.video_file.path)
        convert_720p(instance.video_file.path)
        convert_1080p(instance.video_file.path)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, using, origin, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

            if os.path.isfile(instance.video_file.path[:-4]+'_480p.mp4'):
                os.remove(instance.video_file.path[:-4]+'_480p.mp4')

            if os.path.isfile(instance.video_file.path[:-4]+'_720p.mp4'):
                os.remove(instance.video_file.path[:-4]+'_720p.mp4')

            if os.path.isfile(instance.video_file.path[:-4]+'_1080p.mp4'):
                os.remove(instance.video_file.path[:-4]+'_1080p.mp4')
            print('File deleted:', instance.video_file.path)