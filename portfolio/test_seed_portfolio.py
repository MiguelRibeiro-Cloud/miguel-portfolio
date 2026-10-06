from io import StringIO
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from .content.projects import PROJECTS
from .models import Project, ProjectScreenshot

PROJECT_BY_SLUG = {project["slug"]: project for project in PROJECTS}


class SeedPortfolioCommandTests(TestCase):
    def test_homepage_orders_flagship_first_and_learning_last_after_reseeding(self):
        fog = Project.objects.create(
            slug="the-fog-book-as-code",
            title="Previous Fog title",
            kind=Project.Kind.LEARNING,
            status=Project.Status.EXPERIMENT,
        )
        call_command("seed_portfolio", stdout=StringIO())
        judge = Project.objects.get(slug="the-judge-aita-ai-chatbot")
        self.assertLess(fog.pk, judge.pk)

        response = self.client.get("/")
        self.assertEqual(
            list(response.context["projects"].values_list("slug", flat=True)),
            [
                "sme-process-discovery-agent",
                "ai-incident-processing-pipeline",
                "standardized-reporting-workflow",
                "customer-context-knowledge-capture-tool",
                "livedhere-pt",
                "the-judge-aita-ai-chatbot",
                "the-fog-book-as-code",
            ],
        )
        html = response.content.decode()
        self.assertLess(html.index("SME Process Discovery Agent"), html.index("Standardized Reporting Workflow"))
        self.assertLess(html.index("SME Process Discovery Agent"), html.index("livedhere.pt"))
        self.assertLess(html.index(judge.title), html.index("The Fog — Book as Code"))
        fog.refresh_from_db()
        self.assertEqual(
            (judge.kind, judge.status),
            (Project.Kind.PERSONAL, Project.Status.PRODUCTION),
        )
        self.assertEqual(
            (fog.kind, fog.status),
            (Project.Kind.LEARNING, Project.Status.EXPERIMENT),
        )

    def test_flagship_homepage_card_has_primary_actions_and_technical_signals(self):
        call_command("seed_portfolio", stdout=StringIO())
        project = Project.objects.get(slug="sme-process-discovery-agent")

        response = self.client.get("/")
        html = response.content.decode()

        self.assertEqual(project.kind, Project.Kind.PERSONAL)
        self.assertEqual(project.status, Project.Status.PRODUCTION)
        self.assertContains(response, 'class="project-card project-card--flagship"')
        self.assertContains(response, "Featured project")
        self.assertContains(response, project.summary)
        self.assertContains(
            response,
            'href="https://process-agent.miguelribeiro.dev" target="_blank" rel="noopener noreferrer"',
        )
        self.assertContains(
            response,
            'href="https://github.com/MiguelRibeiro-Cloud/sme-process-agent" target="_blank" rel="noopener noreferrer"',
        )
        self.assertContains(
            response,
            f'href="{reverse("project_detail", args=[project.slug])}">View case study',
        )
        for signal in ("Python", "FastAPI", "GPT", "MCP", "RAG", "AI Evals"):
            with self.subTest(signal=signal):
                self.assertContains(response, signal)
        self.assertLess(html.index(project.title), html.index("livedhere.pt"))

    @override_settings(
        ALLOWED_HOSTS=["portfolio.example"],
        PUBLIC_SITE_URL="https://portfolio.example",
    )
    def test_incident_pipeline_is_second_with_public_actions_and_case_study(self):
        call_command("seed_portfolio", stdout=StringIO())
        project = Project.objects.get(slug="ai-incident-processing-pipeline")

        home = self.client.get("/", HTTP_HOST="portfolio.example")
        html = home.content.decode()
        self.assertEqual(project.kind, Project.Kind.PERSONAL)
        self.assertEqual(project.status, Project.Status.PRODUCTION)
        self.assertContains(home, 'class="project-card project-card--spotlight"')
        self.assertLess(
            html.index("SME Process Discovery Agent"),
            html.index(project.title),
        )
        self.assertLess(
            html.index(project.title),
            html.index("Standardized Reporting Workflow"),
        )
        for tag in ("Celery", "FastAPI", "Redis", "PostgreSQL", "Python", "TypeScript"):
            with self.subTest(tag=tag):
                self.assertContains(home, tag)
        self.assertContains(
            home,
            'href="https://incident.miguelribeiro.dev" target="_blank" rel="noopener noreferrer"',
        )
        self.assertContains(
            home,
            'href="https://github.com/MiguelRibeiro-Cloud/ai-incident-pipeline" target="_blank" rel="noopener noreferrer"',
        )

        path = reverse("project_detail", args=[project.slug])
        detail = self.client.get(path, HTTP_HOST="portfolio.example")
        detail_html = detail.content.decode()
        self.assertTemplateUsed(detail, "portfolio/project_detail_incident.html")
        self.assertInHTML(
            "<title>AI Incident Processing Pipeline | Miguel Ribeiro</title>",
            detail_html,
        )
        self.assertInHTML(
            f'<link rel="canonical" href="https://portfolio.example{path}">',
            detail_html,
        )
        for text in (
            "Long-running AI work needs a different execution model.",
            "PostgreSQL is the durable source of truth.",
            "Selective retries",
            "at-least-once-style execution",
            "Follow the work, not just a spinner.",
            "Deterministic chaos path",
            "A schema at the model boundary.",
            "Observed evidence",
            "AI inference",
            "Cloudflare Workers",
            "Celery 5.6",
        ):
            with self.subTest(text=text):
                self.assertContains(detail, text)
        self.assertContains(detail, "not exactly-once processing")
        self.assertContains(detail, 'class="screenshot-dialog"')
        self.assertContains(detail, "screenshot-gallery.js")

        screenshots = list(
            project.screenshots.values_list("image_path", "caption", "sort_order")
        )
        self.assertEqual([order for _, _, order in screenshots], [1, 2, 3])
        self.assertEqual(
            [path for path, _, _ in screenshots],
            [
                "portfolio/projects/ai-incident-pipeline/chaos-retries.png",
                "portfolio/projects/ai-incident-pipeline/completed-workflow.png",
                "portfolio/projects/ai-incident-pipeline/final-report.png",
            ],
        )
        for screenshot_path, caption, _ in screenshots:
            self.assertIsNotNone(finders.find(screenshot_path))
            self.assertTrue(caption)

    @override_settings(
        ALLOWED_HOSTS=["portfolio.example"],
        PUBLIC_SITE_URL="https://portfolio.example",
    )
    def test_flagship_case_study_route_metadata_and_engineering_story(self):
        call_command("seed_portfolio", stdout=StringIO())
        project = Project.objects.get(slug="sme-process-discovery-agent")
        path = reverse("project_detail", args=[project.slug])

        response = self.client.get(path, HTTP_HOST="portfolio.example")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "portfolio/project_detail_flagship.html")
        self.assertInHTML(
            "<title>SME Process Discovery Agent | Miguel Ribeiro</title>", html
        )
        self.assertInHTML(
            '<meta name="description" content="Evidence-aware AI process discovery using MCP, RAG, structured state, explicit orchestration, and behavioral evaluation.">',
            html,
        )
        self.assertInHTML(
            f'<link rel="canonical" href="https://portfolio.example{path}">', html
        )
        for text in (
            "The agent investigates first.",
            "Application-owned state",
            "Evidence provenance",
            "MCP handles operational capabilities.",
            "ProcessState",
            "Process Analyst",
            "Automation Designer",
            "Evidence Verifier",
            "35/37 behavioral criteria",
            "Public-demo hardening",
            "Northstar Industrial Services is a fictional demo company using synthetic data.",
            "using AI coding agents heavily for implementation",
        ):
            with self.subTest(text=text):
                self.assertContains(response, text)
        self.assertContains(response, 'class="architecture-diagram" role="img"')
        self.assertContains(response, 'class="flagship-visual-grid"')
        for filename in (
            "sme-process-agent-discovery.png",
            "sme-process-agent-process-model.png",
            "sme-process-agent-orchestration.png",
        ):
            self.assertContains(response, filename)
        self.assertContains(
            response,
            'href="https://process-agent.miguelribeiro.dev" target="_blank" rel="noopener noreferrer"',
        )
        self.assertContains(
            response,
            'href="https://github.com/MiguelRibeiro-Cloud/sme-process-agent" target="_blank" rel="noopener noreferrer"',
        )

    def test_seeds_the_fog_without_links_or_screenshots_and_preserves_unrelated_work(self):
        unrelated = Project.objects.create(
            slug="independent-project",
            title="Independent project",
            kind=Project.Kind.PERSONAL,
        )
        unrelated_screenshot = ProjectScreenshot.objects.create(
            project=unrelated,
            image_path="portfolio/projects/independent/overview.png",
            caption="Independent screenshot",
        )

        call_command("seed_portfolio", stdout=StringIO())
        fog = Project.objects.get(slug="the-fog-book-as-code")
        self.assertEqual(fog.title, "The Fog — Book as Code")
        self.assertEqual(fog.kind, Project.Kind.LEARNING)
        self.assertEqual(fog.status, Project.Status.EXPERIMENT)
        self.assertEqual(fog.live_url, "")
        self.assertEqual(fog.source_url, "")
        self.assertFalse(fog.screenshots.exists())

        response = self.client.get(reverse("project_detail", args=[fog.slug]))
        self.assertContains(response, "Learning project")
        self.assertContains(response, "Experiment")
        self.assertContains(response, "Write Chapter X. Follow the repository instructions.")
        self.assertNotContains(response, "Visit live project")
        self.assertNotContains(response, "View source")
        self.assertNotContains(response, 'id="screenshots"')

        project_ids = dict(Project.objects.values_list("slug", "id"))
        call_command("seed_portfolio", stdout=StringIO())

        self.assertEqual(dict(Project.objects.values_list("slug", "id")), project_ids)
        self.assertFalse(fog.screenshots.exists())
        self.assertTrue(Project.objects.filter(pk=unrelated.pk, title="Independent project").exists())
        self.assertTrue(
            ProjectScreenshot.objects.filter(
                pk=unrelated_screenshot.pk,
                caption="Independent screenshot",
            ).exists()
        )

    def test_seeds_the_judge_and_preserves_existing_projects_on_rerun(self):
        unrelated = Project.objects.create(
            slug="independent-project",
            title="Independent project",
            kind=Project.Kind.PERSONAL,
        )
        unrelated_screenshot = ProjectScreenshot.objects.create(
            project=unrelated,
            image_path="portfolio/projects/independent/overview.png",
            caption="Independent screenshot",
        )

        call_command("seed_portfolio", stdout=StringIO())
        judge = Project.objects.get(slug="the-judge-aita-ai-chatbot")
        self.assertEqual(judge.title, "The Judge — AITA AI Chatbot")
        self.assertEqual(judge.kind, Project.Kind.PERSONAL)
        self.assertEqual(judge.status, Project.Status.PRODUCTION)
        self.assertEqual(judge.live_url, "https://www.amitheassholeai.com/")
        self.assertEqual(judge.source_url, "")

        screenshots = list(judge.screenshots.values_list("image_path", "caption", "sort_order"))
        self.assertEqual(len(screenshots), 4)
        self.assertEqual([order for _, _, order in screenshots], [1, 2, 3, 4])
        self.assertEqual(
            [path for path, _, _ in screenshots],
            [
                "portfolio/projects/aitabot/normal.png",
                "portfolio/projects/aitabot/main.png",
                "portfolio/projects/aitabot/prompt_cake_injection.png",
                "portfolio/projects/aitabot/disclaimer.png",
            ],
        )
        self.assertIn("case material", screenshots[2][1])
        for path, caption, _ in screenshots:
            self.assertIsNotNone(finders.find(path))
            self.assertTrue(caption)
        response = self.client.get(reverse("project_detail", args=[judge.slug]))
        self.assertContains(response, 'href="https://www.amitheassholeai.com/"')
        self.assertNotContains(response, "View source")

        project_ids = dict(Project.objects.values_list("slug", "id"))
        screenshot_ids = list(judge.screenshots.values_list("id", flat=True))
        call_command("seed_portfolio", stdout=StringIO())

        self.assertEqual(dict(Project.objects.values_list("slug", "id")), project_ids)
        self.assertEqual(list(judge.screenshots.values_list("id", flat=True)), screenshot_ids)
        self.assertEqual(judge.screenshots.count(), 4)
        self.assertTrue(Project.objects.filter(pk=unrelated.pk, title="Independent project").exists())
        self.assertTrue(
            ProjectScreenshot.objects.filter(
                pk=unrelated_screenshot.pk,
                caption="Independent screenshot",
            ).exists()
        )

    def test_creates_projects_with_complete_case_study_content(self):
        output = StringIO()

        call_command("seed_portfolio", stdout=output)

        self.assertSetEqual(
            set(Project.objects.values_list("slug", flat=True)),
            {project["slug"] for project in PROJECTS},
        )
        for definition in PROJECTS:
            project = Project.objects.get(slug=definition["slug"])
            for field in (
                "title",
                "kind",
                "summary",
                "problem",
                "solution",
                "outcome",
                "lessons",
                "status",
                "live_url",
                "source_url",
            ):
                self.assertEqual(getattr(project, field), definition[field])
            self.assertIn(f"Created: {project.title}", output.getvalue())
        self.assertEqual(
            ProjectScreenshot.objects.count(),
            sum(len(definition["screenshots"]) for definition in PROJECTS),
        )
        livedhere = Project.objects.get(slug="livedhere-pt")
        self.assertEqual(
            list(livedhere.screenshots.values_list("image_path", flat=True)),
            [
                screenshot["image_path"]
                for screenshot in PROJECT_BY_SLUG["livedhere-pt"]["screenshots"]
            ],
        )
        self.assertEqual(
            Project.objects.get(slug="standardized-reporting-workflow").kind,
            Project.Kind.PROFESSIONAL,
        )
        self.assertEqual(
            Project.objects.get(slug="customer-context-knowledge-capture-tool").kind,
            Project.Kind.PROFESSIONAL,
        )
        self.assertEqual(
            Project.objects.get(slug="livedhere-pt").kind,
            Project.Kind.PERSONAL,
        )
        for professional in Project.objects.filter(kind=Project.Kind.PROFESSIONAL):
            self.assertEqual(professional.live_url, "")
            self.assertEqual(professional.source_url, "")
        personal = Project.objects.get(slug="livedhere-pt")
        self.assertEqual(personal.live_url, "https://www.livedhere.pt/en")
        self.assertEqual(personal.source_url, "")

        response = self.client.get(reverse("project_detail", args=[personal.slug]))
        self.assertContains(
            response,
            'href="https://www.livedhere.pt/en" target="_blank" rel="noopener noreferrer"',
        )
        self.assertNotContains(response, "View source")
        self.assertContains(response, 'class="container case-study-layout case-study-layout--visual"')
        self.assertContains(response, 'class="screenshot-dialog"')
        self.assertContains(response, 'screenshot-gallery.js')
        content = response.content.decode()
        paths = [
            screenshot["image_path"]
            for screenshot in PROJECT_BY_SLUG["livedhere-pt"]["screenshots"]
        ]
        self.assertEqual(content.count('class="screenshot-link"'), len(paths))
        self.assertTrue(
            content.index(paths[0]) < content.index(paths[1]) < content.index(paths[2])
        )
        for path in paths:
            self.assertIsNotNone(finders.find(path))
        self.assertIsNotNone(finders.find("portfolio/screenshot-gallery.js"))

    def test_second_run_updates_without_creating_duplicates(self):
        call_command("seed_portfolio", stdout=StringIO())
        original_ids = dict(Project.objects.values_list("slug", "id"))
        output = StringIO()

        call_command("seed_portfolio", stdout=output)

        self.assertEqual(Project.objects.count(), len(PROJECTS))
        self.assertEqual(dict(Project.objects.values_list("slug", "id")), original_ids)
        for definition in PROJECTS:
            self.assertIn(f"Updated: {definition['title']}", output.getvalue())

    def test_updates_existing_project_without_deleting_unrelated_records(self):
        definition = PROJECTS[0]
        existing = Project.objects.create(
            slug=definition["slug"],
            title="Old title",
            summary="Old summary",
            status=Project.Status.LEARNING,
        )
        original_id = existing.pk
        unrelated = Project.objects.create(slug="other-work", title="Other work")

        call_command("seed_portfolio", stdout=StringIO())

        existing.refresh_from_db()
        self.assertEqual(existing.pk, original_id)
        self.assertEqual(existing.title, definition["title"])
        self.assertEqual(existing.summary, definition["summary"])
        self.assertEqual(existing.status, definition["status"])
        self.assertTrue(Project.objects.filter(pk=unrelated.pk).exists())

    def test_screenshots_are_synchronized_without_duplicates(self):
        definition = {
            **PROJECT_BY_SLUG["livedhere-pt"],
            "screenshots": (
                {
                    "image_path": "portfolio/projects/livedhere/overview.png",
                    "caption": "Overview",
                    "sort_order": 1,
                },
            ),
        }
        with patch(
            "portfolio.management.commands.seed_portfolio.PROJECTS",
            (definition,),
        ):
            call_command("seed_portfolio", stdout=StringIO())
            call_command("seed_portfolio", stdout=StringIO())

        screenshot = ProjectScreenshot.objects.get()
        self.assertEqual(ProjectScreenshot.objects.count(), 1)
        self.assertEqual(screenshot.caption, "Overview")

        updated = {
            **definition,
            "screenshots": (
                {**definition["screenshots"][0], "caption": "Updated overview", "sort_order": 2},
            ),
        }
        with patch(
            "portfolio.management.commands.seed_portfolio.PROJECTS",
            (updated,),
        ):
            call_command("seed_portfolio", stdout=StringIO())

        screenshot.refresh_from_db()
        self.assertEqual(ProjectScreenshot.objects.count(), 1)
        self.assertEqual(screenshot.caption, "Updated overview")
        self.assertEqual(screenshot.sort_order, 2)

        unrelated = Project.objects.create(
            slug="other-personal-project",
            title="Other personal project",
            kind=Project.Kind.PERSONAL,
        )
        unrelated_screenshot = ProjectScreenshot.objects.create(
            project=unrelated,
            image_path="portfolio/projects/other/overview.png",
        )
        with patch(
            "portfolio.management.commands.seed_portfolio.PROJECTS",
            ({**definition, "screenshots": ()},),
        ):
            call_command("seed_portfolio", stdout=StringIO())

        self.assertFalse(ProjectScreenshot.objects.filter(pk=screenshot.pk).exists())
        self.assertTrue(
            ProjectScreenshot.objects.filter(pk=unrelated_screenshot.pk).exists()
        )

    def test_professional_projects_cannot_seed_screenshots(self):
        definition = {
            **PROJECT_BY_SLUG["standardized-reporting-workflow"],
            "screenshots": ({"image_path": "portfolio/projects/private.png"},),
        }

        with patch(
            "portfolio.management.commands.seed_portfolio.PROJECTS",
            (definition,),
        ):
            with self.assertRaises(CommandError):
                call_command("seed_portfolio", stdout=StringIO())

        self.assertFalse(Project.objects.exists())
