from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from backend.permissions import IsAdminOrReadOnly
from .models import Category, Post, Tag
from .serializers import CategorySerializer, PostListSerializer, PostSerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_object(self):
        lookup_value = self.kwargs.get('pk')
        queryset = self.filter_queryset(self.get_queryset())

        if str(lookup_value).isdigit():
            obj = get_object_or_404(queryset, pk=lookup_value)
        else:
            obj = get_object_or_404(queryset, slug=lookup_value)

        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
