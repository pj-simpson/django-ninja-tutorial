from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from ninja_service.models import Project, Release

from .serializers import ProjectSerializer, ReleaseSerializer


class CustomPagination(PageNumberPagination):
    page_size = 3


class ProjectsList(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ReleaseList(ListCreateAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    pagination_class = CustomPagination


class ReleaseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
