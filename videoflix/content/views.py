from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Video, VideoProgress
from .serializers import VideoSerializer, VideoProgressSerializer

CustomUser = get_user_model()
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class VideoProgressViewSet(viewsets.ModelViewSet):
    queryset = VideoProgress.objects.all()
    serializer_class = VideoProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the logged-in user's progress
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        video_id = self.request.data.get('video_id')
        if not video_id:
            raise serializers.ValidationError({'video_id': 'This field is required.'})
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise serializers.ValidationError({'video': 'Video not found.'})

        # Speichern mit automatisch gesetztem `user` und `video`
        serializer.save(user=self.request.user, video=video)

    @action(detail=False, methods=['post'])
    def update_progress(self, request):
        user = request.user
        video_id = request.data.get('video_id')
        played_time = request.data.get('played_time')
    
        if not video_id or played_time is None:
            return Response({'error': 'video_id and played_time are required'}, status=400)
    
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)
    
        # Update or create progress
        progress, created = VideoProgress.objects.update_or_create(
            user=user,
            video=video,
            defaults={'played_time': played_time}
        )
    
        return Response(VideoProgressSerializer(progress).data)

