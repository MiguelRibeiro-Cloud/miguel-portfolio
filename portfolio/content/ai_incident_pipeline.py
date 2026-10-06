"""Public, version-controlled content for the AI incident pipeline case study."""

SLUG = "ai-incident-processing-pipeline"

PROJECT = {
    "slug": SLUG,
    "kind": "personal",
    "title": "AI Incident Processing Pipeline",
    "summary": (
        "A distributed AI incident-processing pipeline built with Celery, Redis, "
        "and FastAPI. It fans service analysis across parallel workers, coordinates "
        "results through a chord, and demonstrates retries, worker recovery, and "
        "idempotent state handling."
    ),
    "problem": (
        "Long-running AI calls are a poor fit for synchronous request/response "
        "execution. An incident-analysis workflow can also fail partway through, "
        "lose a worker, or receive the same task more than once. The project explores "
        "how to move that work into an asynchronous pipeline without losing durable "
        "state or hiding partial failure from the user."
    ),
    "solution": (
        "FastAPI creates a durable job in PostgreSQL before Celery starts the work. "
        "Deterministic normalization and summarization run as a chain, then service "
        "analyses fan out dynamically through a Celery group. Redis transports tasks "
        "and temporarily coordinates chord results; the chord releases a final Gemini "
        "synthesis only after every service branch returns. PostgreSQL remains the "
        "durable source of truth throughout.\n\n"
        "Retries are limited to transient provider and network failures, with bounded "
        "attempts, exponential backoff, and jitter. Late acknowledgements, "
        "reject-on-worker-lost behavior, a prefetch multiplier of one, terminal-state "
        "guards, and idempotent service-analysis persistence support safe recovery "
        "under at-least-once-style execution semantics."
    ),
    "outcome": (
        "The deployed public demo exposes the workflow instead of hiding it behind a "
        "spinner. Visitors can follow normalization, summarization, parallel service "
        "branches, chord coordination, and final synthesis. A deterministic chaos "
        "mode injects two temporary checkout-api failures before Gemini is called, "
        "making the retries and third-attempt recovery visible.\n\n"
        "Gemini responses use a standard JSON Schema and are validated with Pydantic. "
        "The interface deliberately separates observed evidence from AI inference."
    ),
    "lessons": (
        "Reliable asynchronous work depends on explicit ownership boundaries. Redis "
        "is useful for task transport and temporary chord coordination, while durable "
        "job and event history belongs in PostgreSQL. At-least-once execution also "
        "makes idempotent state changes and terminal-state guards part of the core "
        "design rather than optional hardening."
    ),
    "status": "production",
    "live_url": "https://incident.miguelribeiro.dev",
    "source_url": "https://github.com/MiguelRibeiro-Cloud/ai-incident-pipeline",
    "screenshots": (
        {
            "image_path": (
                "portfolio/projects/ai-incident-pipeline/chaos-retries.png"
            ),
            "caption": (
                "The chaos workflow with two checkout-api retries visible while the "
                "Celery chord holds final synthesis."
            ),
            "sort_order": 1,
        },
        {
            "image_path": (
                "portfolio/projects/ai-incident-pipeline/completed-workflow.png"
            ),
            "caption": (
                "The completed chain, parallel service group, chord convergence, and "
                "final synthesis."
            ),
            "sort_order": 2,
        },
        {
            "image_path": (
                "portfolio/projects/ai-incident-pipeline/final-report.png"
            ),
            "caption": (
                "Service-level results keep observed evidence separate from AI "
                "inference before the final incident intelligence report."
            ),
            "sort_order": 3,
        },
    ),
}

CASE_STUDY = {
    "kicker": "Distributed asynchronous processing",
    "meta_description": (
        "A distributed Celery pipeline for observable, retryable AI workloads with "
        "parallel processing, idempotent persistence, and worker-loss recovery."
    ),
    "domain": "incident.miguelribeiro.dev",
    "card_tags": ("Celery", "FastAPI", "Redis", "PostgreSQL", "Python", "TypeScript"),
    "architecture": (
        {"label": "Request", "value": "Browser → FastAPI"},
        {"label": "Durable job", "value": "PostgreSQL"},
        {"label": "Task transport", "value": "Redis → Celery"},
        {"label": "Deterministic work", "value": "Normalize → Summarize"},
        {"label": "Parallel work", "value": "Dynamic service-analysis group"},
        {"label": "Fan-in", "value": "Redis result backend → Celery chord"},
        {"label": "Final work", "value": "Gemini synthesis → PostgreSQL"},
    ),
    "architecture_caption": (
        "PostgreSQL is the durable source of truth. Redis carries tasks and holds "
        "temporary result state needed for chord coordination."
    ),
    "reliability": (
        {
            "title": "Selective retries",
            "copy": (
                "Only transient provider and network failures retry, using bounded "
                "attempts, exponential backoff, and jitter."
            ),
        },
        {
            "title": "Worker-loss recovery",
            "copy": (
                "Late acknowledgements and reject-on-worker-lost behavior allow lost "
                "work to be redelivered. Worker prefetch is limited to one task."
            ),
        },
        {
            "title": "Idempotent persistence",
            "copy": (
                "Service-analysis writes and terminal-state guards are designed for "
                "at-least-once-style execution, not exactly-once processing."
            ),
        },
        {
            "title": "Durable history",
            "copy": (
                "Job state and execution events are persisted so progress and failure "
                "remain inspectable outside worker memory."
            ),
        },
    ),
    "workflow": (
        "Normalize incident events",
        "Build a deterministic summary",
        "Fan service analyses out in parallel",
        "Wait for every branch in a chord",
        "Run final Gemini synthesis",
    ),
    "chaos": (
        "The chaos demo injects temporary failures before Gemini is called for "
        "checkout-api. Attempts one and two fail, Celery schedules real retries, "
        "attempt three succeeds, and the waiting chord then releases final synthesis."
    ),
    "structured_ai": (
        (
            "Gemini 3.5 Flash Lite receives a standard JSON Schema for each structured "
            "response. Returned data is then validated through Pydantic before it can "
            "be persisted or presented."
        ),
        (
            "The interface keeps source observations visually distinct from model "
            "inference. That makes it clearer which claims came from the incident "
            "payload and which were proposed by the AI analysis."
        ),
    ),
    "deployment": (
        {
            "label": "Frontend",
            "items": "React, TypeScript, Vite, TanStack Query, Cloudflare Workers static assets",
        },
        {
            "label": "Railway",
            "items": "FastAPI service, separate Celery worker, managed Redis, managed PostgreSQL",
        },
        {
            "label": "AI execution",
            "items": "Gemini 3.5 Flash Lite calls from Celery workers",
        },
    ),
    "stack": (
        {"label": "Backend", "items": "Python, FastAPI, Celery 5.6, SQLAlchemy, Alembic, Pydantic"},
        {"label": "State & coordination", "items": "PostgreSQL, Redis, Celery chain/group/chord"},
        {"label": "Frontend", "items": "React, TypeScript, Vite, TanStack Query"},
        {"label": "Deployment", "items": "Docker, Railway, Cloudflare Workers"},
    ),
}
