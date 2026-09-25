from django.test import TestCase
from django.urls import reverse

from .models import Project


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

    def test_project_detail_loads(self):
        response = self.client.get(
            reverse("project_detail", args=[self.project.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_missing_project_returns_404(self):
        response = self.client.get("/projects/does-not-exist/")

        self.assertEqual(response.status_code, 404)