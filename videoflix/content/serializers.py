from rest_framework import serializers
from .models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoProgressSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()  # Optional: Replace with UserSerializer if needed
    # video = serializers.StringRelatedField()  # Optional: Replace with VideoSerializer if needed

    class Meta:
        model = VideoProgress
        fields = '__all__'
        read_only_fields = ['last_updated']