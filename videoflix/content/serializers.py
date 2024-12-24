from rest_framework import serializers
from .models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['played_time']  # Nur `played_time` als Eingabefeld zulassen
        read_only_fields = ['user', 'video', 'last_updated']  # Diese Felder sind nur lesbar