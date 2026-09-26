from django.test import TestCase
from django.urls import reverse

from .models import Project, ProjectScreenshot


class HealthViewTests(TestCase):
    def test_health_returns_ok(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class PortfolioViewTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            summary="A project created for automated testing.",
        )

    def test_homepage_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_homepage_shows_project(self):
        response = self.client.get("/")

        self.assertContains(response, "Test Project")

    def test_homepage_card_uses_project_data_and_links_to_detail(self):
        response = self.client.get("/")

        self.assertContains(response, self.project.summary)
        self.assertContains(response, self.project.get_status_display())
        self.assertContains(response, "Professional project")
        self.assertContains(
            response,
            f'<a class="project-card-link" href="{reverse("project_detail", args=[self.project.slug])}"',
        )
        self.assertContains(response, "Read case study")
        self.assertEqual(
            response.content.decode().count(
                f'href="{reverse("project_detail", args=[self.project.slug])}"'
            ),
            1,
        )

    def test_learning_project_kind_is_displayed(self):
        self.project.kind = Project.Kind.LEARNING
        self.project.save()

        response = self.client.get("/")

        self.assertContains(response, "Learning project")

    def test_project_detail_loads(self):
        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_project_detail_only_links_to_populated_sections(self):
        self.project.problem = "The source workflow required manual work."
        self.project.save()

        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertContains(response, self.project.problem)
        self.assertContains(response, 'href="#problem"')
        self.assertNotContains(response, 'href="#solution"')
        self.assertNotContains(response, 'id="solution"')

    def test_personal_project_displays_optional_urls_and_screenshots(self):
        self.project.kind = Project.Kind.PERSONAL
        self.project.live_url = "https://example.com/live"
        self.project.source_url = "https://github.com/example/source"
        self.project.save()
        ProjectScreenshot.objects.create(
            project=self.project,
            image_path="portfolio/projects/example.png",
            caption="Application home screen",
        )

        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertContains(response, "Personal project")
        self.assertContains(response, 'href="#screenshots"')
        self.assertContains(response, 'src="/static/portfolio/projects/example.png"')
        self.assertContains(response, "Application home screen")
        self.assertContains(
            response,
            'href="https://example.com/live" target="_blank" rel="noopener noreferrer"',
        )
        self.assertContains(
            response,
            'href="https://github.com/example/source" target="_blank" rel="noopener noreferrer"',
        )

    def test_personal_project_omits_empty_visuals_and_actions(self):
        self.project.kind = Project.Kind.PERSONAL
        self.project.save()

        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertNotContains(response, 'id="screenshots"')
        self.assertNotContains(response, "Visit live project")
        self.assertNotContains(response, "View source")

    def test_professional_project_never_displays_visuals_or_external_actions(self):
        self.project.live_url = "https://example.com/internal"
        self.project.source_url = "https://example.com/source"
        self.project.save()
        ProjectScreenshot.objects.create(
            project=self.project,
            image_path="portfolio/projects/private.png",
            caption="Should stay private",
        )

        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertContains(response, "Professional project")
        self.assertNotContains(response, "Should stay private")
        self.assertNotContains(response, "private.png")
        self.assertNotContains(response, "https://example.com/internal")
        self.assertNotContains(response, "https://example.com/source")

    def test_missing_project_returns_404(self):
        response = self.client.get("/projects/does-not-exist/")

        self.assertEqual(response.status_code, 404)
