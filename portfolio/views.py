import json

from django.core.exceptions import RequestDataTooBig
from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .canonical import canonical_url
from .content.ai_incident_pipeline import (
    CASE_STUDY as INCIDENT_CASE_STUDY,
    SLUG as INCIDENT_SLUG,
)
from .content.sme_process_agent import CASE_STUDY, SLUG as FLAGSHIP_SLUG
from .models import Project
from .services.assistant import answer
from .services.google_ai import AssistantConfigurationError, AssistantProviderError


MAX_BODY_BYTES = 12_000
MAX_MESSAGE_LENGTH = 1_000
MAX_HISTORY_TURNS = 8
MAX_HISTORY_CHARACTERS = 5_000


def _page_metadata(request, title, description, og_type):
    return {
        "page_title": title,
        "page_description": description,
        "canonical_url": canonical_url(request),
        "og_type": og_type,
    }


def home(request):
    projects = Project.objects.annotate(
        featured_order=Case(
            When(slug=FLAGSHIP_SLUG, then=Value(0)),
            When(slug=INCIDENT_SLUG, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        ),
        kind_order=Case(
            When(kind=Project.Kind.PROFESSIONAL, then=Value(0)),
            When(kind=Project.Kind.PERSONAL, then=Value(1)),
            When(kind=Project.Kind.LEARNING, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    ).order_by("featured_order", "kind_order", "id")
    context = {
        "projects": projects,
        "flagship_slug": FLAGSHIP_SLUG,
        "flagship": CASE_STUDY,
        "incident_slug": INCIDENT_SLUG,
        "incident": INCIDENT_CASE_STUDY,
        **_page_metadata(
            request,
            "Miguel Ribeiro | Automation, Software and Cloud",
            "Miguel Ribeiro builds automation, data workflows and Python-backed "
            "applications for operational problems.",
            "website",
        ),
    }
    return render(request, "portfolio/home.html", context)


def health(request):
    return JsonResponse({"status": "ok"})


@require_POST
def assistant_chat(request):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Send a JSON request."}, status=415)
    content_length = request.META.get("CONTENT_LENGTH", "")
    if content_length.isdigit() and int(content_length) > MAX_BODY_BYTES:
        return JsonResponse({"error": "The request is too large."}, status=413)
    try:
        body = request.body
    except RequestDataTooBig:
        return JsonResponse({"error": "The request is too large."}, status=413)
    if len(body) > MAX_BODY_BYTES:
        return JsonResponse({"error": "The request is too large."}, status=413)

    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "Send valid JSON."}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "Send a JSON object."}, status=400)

    message = payload.get("message")
    history = payload.get("history", [])
    if (
        not isinstance(message, str)
        or not message.strip()
        or len(message) > MAX_MESSAGE_LENGTH
    ):
        return JsonResponse({"error": "Enter a message of up to 1,000 characters."}, status=400)
    if not isinstance(history, list) or len(history) > MAX_HISTORY_TURNS:
        return JsonResponse({"error": "Conversation history is invalid."}, status=400)
    invalid_turn = any(
        not isinstance(turn, dict)
        or turn.get("role") not in ("user", "assistant")
        or not isinstance(turn.get("content"), str)
        or not turn["content"].strip()
        or len(turn["content"]) > MAX_MESSAGE_LENGTH
        for turn in history
    )
    if invalid_turn:
        return JsonResponse({"error": "Conversation history is invalid."}, status=400)
    if (
        len(history) % 2
        or any(
            turn["role"] != ("user" if index % 2 == 0 else "assistant")
            for index, turn in enumerate(history)
        )
        or sum(len(turn["content"]) for turn in history) > MAX_HISTORY_CHARACTERS
    ):
        return JsonResponse({"error": "Conversation history is invalid."}, status=400)

    try:
        reply = answer(message.strip(), history)
    except AssistantConfigurationError:
        return JsonResponse({"error": "The assistant is temporarily unavailable."}, status=503)
    except AssistantProviderError:
        return JsonResponse({"error": "The assistant could not answer right now. Please try again."}, status=502)
    return JsonResponse({"reply": reply})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    is_flagship = project.slug == FLAGSHIP_SLUG
    is_incident = project.slug == INCIDENT_SLUG
    screenshots = (
        project.screenshots.all()
        if project.kind == Project.Kind.PERSONAL
        else ()
    )
    context = {
        "project": project,
        "screenshots": screenshots,
        "flagship": CASE_STUDY if is_flagship else None,
        "incident": INCIDENT_CASE_STUDY if is_incident else None,
        **_page_metadata(
            request,
            f"{project.title} | Miguel Ribeiro",
            (
                CASE_STUDY["meta_description"]
                if is_flagship
                else INCIDENT_CASE_STUDY["meta_description"]
                if is_incident
                else project.summary.strip()
                or f"Case study of {project.title} by Miguel Ribeiro."
            ),
            "article",
        ),
    }
    if is_flagship:
        template = "portfolio/project_detail_flagship.html"
    elif is_incident:
        template = "portfolio/project_detail_incident.html"
    else:
        template = "portfolio/project_detail.html"
    return render(request, template, context)
