from django.urls import path

from .views import assistant_chat, health, home, project_detail

urlpatterns = [
    path("", home),
    path("health/", health),
    path("api/assistant/chat/", assistant_chat, name="assistant_chat"),
    path(
    "projects/<slug:slug>/",
    project_detail,
    name="project_detail",
),
]
