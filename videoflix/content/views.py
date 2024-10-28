from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .models import Video
from .serializers import VideoSerializer, PasswordResetSerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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
    
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate a reset token or code here. This could be a unique URL or a code
                reset_token = get_random_string(20)
                
                # Save reset token to user profile or a separate model for tracking
                # user.profile.reset_token = reset_token
                # user.profile.save()

                # Send reset email
                reset_url = f"http://localhost:4200/resetpassword?token={reset_token}"
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_url}',
                    'noreply@yourdomain.com',
                    [email],
                    fail_silently=False,
                )
                
                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        # Find user by token and update password
        try:
            user = User.objects.get(profile__reset_token=token)
            user.set_password(new_password)
            user.profile.reset_token = ''  # Clear token after successful reset
            user.profile.save()
            user.save()
            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

