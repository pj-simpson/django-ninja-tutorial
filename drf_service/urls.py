from django.urls import path

from .views import ProjectDetail, ProjectsList, ReleaseDetail, ReleaseList

urlpatterns = [
    path("projects/<int:pk>", ProjectDetail.as_view(), name="project_detail"),
    path("projects", ProjectsList.as_view(), name="project_list"),
    path("releases/<int:pk>", ReleaseDetail.as_view(), name="release_detail"),
    path("releases", ReleaseList.as_view(), name="release_list"),
]
