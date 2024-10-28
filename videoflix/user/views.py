from django.shortcuts import render

from rest_framework import viewsets, status, generics
from django.contrib.auth import get_user_model, authenticate
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

CustomUser = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer dürfen darauf zugreifen

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        token_header = request.headers.get('Authorization')

        if token_header and token_header.startswith('Token '):
            token_key = token_header.split(' ')[1]  # Token aus dem Header extrahieren
            try:
                # Versuche, den Token zu finden und den Benutzer zu authentifizieren
                token = Token.objects.get(key=token_key)
                user = token.user
                return Response({'token': token.key, "Success": "User automatically authenticated"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'message': 'Invalid token'}, status=401)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                # Benutzer anhand der E-Mail-Adresse finden
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Invalid email or password'}, status=401)

            # Benutzer authentifizieren
            user = authenticate(username=user.username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, "Success": "Login Successfully"}, status=status.HTTP_201_CREATED)
            
            return Response({'message': 'Invalid email or password'}, status=401)