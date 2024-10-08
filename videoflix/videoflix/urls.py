"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from content.views import VideoViewSet
from user.views import CustomUserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('videoflix/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
