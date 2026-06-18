from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from backend.permissions import IsAdminOrReadOnly
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        lookup_value = self.kwargs.get('pk')
        queryset = self.filter_queryset(self.get_queryset())

        if str(lookup_value).isdigit():
            obj = get_object_or_404(queryset, pk=lookup_value)
        else:
            obj = get_object_or_404(queryset, slug=lookup_value)

        self.check_object_permissions(self.request, obj)
        return obj
