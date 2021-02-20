from rest_framework import serializers

from ninja_service.models import Project, Release


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("id",)


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = "__all__"
        read_only_fields = ("id",)
