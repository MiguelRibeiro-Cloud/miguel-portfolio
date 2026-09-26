from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Project
from django.shortcuts import get_object_or_404, render


def home(request):
    projects = Project.objects.all()
    return render(request, "portfolio/home.html", {"projects": projects})


def health(request):
    return JsonResponse({"status": "ok"})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    screenshots = (
        project.screenshots.all()
        if project.kind == Project.Kind.PERSONAL
        else ()
    )
    return render(
        request,
        "portfolio/project_detail.html",
        {"project": project, "screenshots": screenshots},
    )
