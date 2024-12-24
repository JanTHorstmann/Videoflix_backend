from rest_framework import serializers
from .models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoProgressSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(source='video.id', read_only=True)
    class Meta:
        model = VideoProgress
        fields = ['video_id', 'played_time', 'duration']  # Nur `played_time` als Eingabefeld zulassen
        read_only_fields = ['user', 'video', 'last_updated']  # Diese Felder sind nur lesbar