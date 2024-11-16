from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .models import Video
from .serializers import VideoSerializer, PasswordResetSerializer
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate
from django.template.loader import render_to_string

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
    
class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                user.set_reset_token()

                reset_url = f"http://localhost:4200/resetpassword?token={user.reset_token}"
                html_content = render_to_string("password_reset_email.html", {
                    "user": user,
                    "reset_url": reset_url
                })

                subject = "Reset your Password"
                from_email = "noreply@videoflix.com"
                email_message = EmailMultiAlternatives(subject, "", from_email, [email])
                email_message.attach_alternative(html_content, "text/html")
                email_message.send()
                
                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.GET.get("token")
        new_password = request.data.get('new_password')
        print(new_password)
        print(token)
        # Find user by token and update password
        try:
            user = CustomUser.objects.get(reset_token=token)
            user.set_password(new_password)
            user.reset_token = ''  # Clear token after successful reset
            user.save()
            # user.save()
            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

