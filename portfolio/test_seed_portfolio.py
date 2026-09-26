from io import StringIO
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from .content.projects import PROJECTS
from .models import Project, ProjectScreenshot


class SeedPortfolioCommandTests(TestCase):
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
            [screenshot["image_path"] for screenshot in PROJECTS[2]["screenshots"]],
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
        paths = [screenshot["image_path"] for screenshot in PROJECTS[2]["screenshots"]]
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
            **PROJECTS[2],
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
            **PROJECTS[0],
            "screenshots": ({"image_path": "portfolio/projects/private.png"},),
        }

        with patch(
            "portfolio.management.commands.seed_portfolio.PROJECTS",
            (definition,),
        ):
            with self.assertRaises(CommandError):
                call_command("seed_portfolio", stdout=StringIO())

        self.assertFalse(Project.objects.exists())
