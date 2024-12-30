from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
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
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Return only the logged-in user's progress
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        video_id = self.request.data.get('video_id')
        played_time = self.request.data.get('played_time')  # Optional: Default to 0
        duration = self.request.data.get('duration')       # Optional: Default to 0

        if not video_id:
            raise serializers.ValidationError({'video_id': 'This field is required.'})

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise serializers.ValidationError({'video': 'Video not found.'})

        # Update or create VideoProgress
        progress, created = VideoProgress.objects.update_or_create(
            user=self.request.user,
            video=video,
            defaults={
                'played_time': played_time,
                'duration': duration,
            }
        )
        # Set the serializer instance to the created or updated object
        serializer.instance = progress

    @action(detail=True, methods=['delete'])
    def delete_progress(self, request, pk=None):
        try:
            # Suche das Video basierend auf der ID (pk)
            video = Video.objects.get(id=pk)
            
            # Finde den zugehörigen VideoProgress für den Benutzer und das Video
            progress = VideoProgress.objects.get(video=video, user=request.user)
            
            # Lösche den gefundenen VideoProgress
            progress.delete()
            return Response({'message': 'Progress deleted successfully'}, status=204)
        
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=404)
        except VideoProgress.DoesNotExist:
            return Response({'error': 'Progress not found or access denied'}, status=404)

