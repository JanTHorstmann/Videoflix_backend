from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import get_user_model, authenticate
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer, PasswordResetSerializer

CustomUser = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Benutzer speichern
        user.confirmed = False
        user.confirmation_token = get_random_string(20)
        user.save()
        confirmation_url = f"https://videoflix.jan-horstmann.eu/confirm_email?token={user.confirmation_token}"

        # E-Mail senden
        html_content = render_to_string("email_confirmation.html", {
            "user": user,
            "confirmation_url": confirmation_url
        })
        subject = "Confirm your email"
        email_message = EmailMultiAlternatives(subject, "", "noreply@videoflix.com", [user.email])
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return Response({"message": "Registration successful! Please check your email to confirm your account."}, status=status.HTTP_201_CREATED)

class ConfirmEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        user = get_object_or_404(CustomUser, confirmation_token=token)
        
        # Bestätigen
        user.confirmed = True
        user.confirmation_token = None  # Token löschen, wenn bestätigt
        user.save()

        return Response({"message": "Email confirmed! You can now log in."}, status=status.HTTP_200_OK)
    
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        token_header = request.headers.get('Authorization')
        if token_header and token_header.startswith('Token '):
            token_key = token_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if not user.confirmed:
                    return Response({"error": "Please confirm your email to log in."}, status=status.HTTP_403_FORBIDDEN)
                return Response({'token': token.key, "Success": "User automatically authenticated"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Invalid email or password'}, status=401)
            if not user.confirmed:
                return Response({"error": "Please confirm your email to log in."}, status=status.HTTP_403_FORBIDDEN)

            user = authenticate(username=user.username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, "Success": "Login Successfully"}, status=status.HTTP_201_CREATED)
            
            return Response({'message': 'Invalid email or password'}, status=401)
        
class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                user.set_reset_token()

                reset_url = f"https://videoflix.jan-horstmann.eu/resetpassword?token={user.reset_token}"
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
        try:
            user = CustomUser.objects.get(reset_token=token)
            user.set_password(new_password)
            user.reset_token = ''
            user.save()
            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)