from django.urls import path

from .views import health, home, project_detail

urlpatterns = [
    path("", home),
    path("health/", health),
    path("projects/<slug:slug>/", project_detail),
]