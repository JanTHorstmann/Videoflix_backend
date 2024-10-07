from django.shortcuts import render

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated

# Das benutzerdefinierte User-Modell abrufen
CustomUser = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer dürfen darauf zugreifen

