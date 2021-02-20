from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from ninja_service.api import api

schema_view = get_schema_view(
    openapi.Info(
        title="DRF Example",
        default_version="v1",
        description="A DRF service to accompany the Django Ninja Tutorial",
        contact=openapi.Contact(email="your_name@example.com"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ninja-api/", api.urls),
    path("drf-api/", include("drf_service.urls")),
    path(
        "drf-api/docs",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
