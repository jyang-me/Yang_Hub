"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts.views import CurrentUserView
from blog.models import Post
from blog.views import CategoryViewSet, PostViewSet, TagViewSet
from contact.models import Message
from contact.views import MessageViewSet
from portfolio.models import Project
from portfolio.views import ProjectViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('posts', PostViewSet)
router.register('projects', ProjectViewSet)
router.register('messages', MessageViewSet)


class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                'posts_count': Post.objects.filter(status='published').count(),
                'projects_count': Project.objects.count(),
                'messages_count': Message.objects.count(),
            }
        )

urlpatterns = [
    path(settings.DJANGO_ADMIN_PATH, admin.site.urls),
    path('api/auth/token/', obtain_auth_token),
    path('api/auth/me/', CurrentUserView.as_view()),
    path('api/stats/', StatsView.as_view()),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
