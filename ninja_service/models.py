from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)


class Release(models.Model):

    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    press_release = models.TextField(null=True)
    release_date = models.DateField()
