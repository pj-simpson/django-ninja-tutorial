from datetime import date
from typing import List

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ninja import File, Form, NinjaAPI, Schema
from ninja.files import UploadedFile

from .models import Project, Release

api = NinjaAPI()


class ProjectIn(Schema):
    name: str
    description: str = None


class ProjectPartialUpdate(Schema):
    name: str = None
    description: str = None


class ProjectOut(Schema):
    id: int
    name: str
    description: str


@api.post("/projects", tags=["projects"])
def create_project(request, payload: ProjectIn):
    project = Project.objects.create(**payload.dict())
    return {"message": f"successfully created project id: {project.id}"}


@api.get("/projects/{project_id}", response=ProjectOut, tags=["projects"])
def get_project(request, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    return project


@api.api_operation(["PUT", "PATCH"], "/projects/{project_id}", tags=["projects"])
def update_project(request, project_id: int, payload: ProjectPartialUpdate):
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        if value:
            setattr(project, attr, value)
    project.save()
    return {"message": f"successfully updated project id: {project.id}"}


@api.delete("/projects/{project_id}", tags=["projects"])
def delete_project(request, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"message": f"successfully deleted project id: {project_id}"}


@api.get("/projects", response=List[ProjectOut], tags=["projects"])
def list_projects(request):
    qs = Project.objects.all()
    return qs


class ReleaseIn(Schema):
    title: str
    project: int
    press_release: str
    release_date: date


class ReleaseUpdate(Schema):
    title: str = None
    project: int = None
    press_release: str = None
    release_date: date = None


class ReleaseOut(Schema):
    id: int
    title: str
    project: ProjectOut
    press_release: str = None
    release_date: date


class PaginatedReleaseOut(Schema):
    total_releases: int
    total_pages: int
    per_page: int
    has_next: bool
    has_previous: bool
    results: List[ReleaseOut] = None


@api.post("/releases", tags=["releases"])
def create_release(request, payload: ReleaseIn):

    release = Release.objects.create(
        project=get_object_or_404(Project, id=payload.project),
        press_release=payload.press_release,
        title=payload.title,
        release_date=payload.release_date,
    )
    return {"message": f"successfully created release id: {release.id}"}


@api.get("/releases/{release_id}", response=ReleaseOut, tags=["releases"])
def get_release(request, release_id: int):
    release = get_object_or_404(Release, id=release_id)
    return release


@api.api_operation(["PUT", "PATCH"], "/releases/{release_id}", tags=["releases"])
def update_release(request, release_id: int, payload: ReleaseUpdate):
    release = get_object_or_404(Release, id=release_id)
    if payload.project:
        release.project = get_object_or_404(Project, id=release.project.id)
    if payload.title:
        release.title = payload.title
    if payload.press_release:
        release.press_release = payload.press_release
    if payload.release_date:
        release.release_date = payload.release_date
    release.save()
    return {"message": f"successfully updated release id: {release.id}"}


@api.delete("/releases/{release_id}", tags=["releases"])
def delete_release(request, release_id: int):
    release = get_object_or_404(Release, id=release_id)
    release.delete()
    return {"message": f"successfully deleted project id: {release.id}"}


@api.get("/releases", response=PaginatedReleaseOut, tags=["releases"])
def list_releases(request, page: int = 1):
    releases = Release.objects.all().order_by("-release_date")
    paginator = Paginator(releases, 3)
    page_number = page
    page_object = paginator.get_page(page_number)
    response = {}
    response["total_releases"] = page_object.paginator.count
    response["total_pages"] = page_object.paginator.num_pages
    response["per_page"] = page_object.paginator.per_page
    response["has_next"] = page_object.has_next()
    response["has_previous"] = page_object.has_previous()
    response["results"] = [i for i in page_object.object_list.values()]
    return response
