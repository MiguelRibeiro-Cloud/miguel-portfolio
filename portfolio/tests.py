import os
import runpy
from unittest.mock import patch

from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .models import Project, ProjectScreenshot


class SecuritySettingsTests(SimpleTestCase):
    def settings_for(self, debug):
        with patch.dict(os.environ, {"DJANGO_DEBUG": debug}):
            return runpy.run_path(str(settings.BASE_DIR / "config" / "settings.py"))

    def test_production_uses_railway_https_header_and_secure_cookies(self):
        production = self.settings_for("False")

        self.assertFalse(production["DEBUG"])
        self.assertEqual(
            production["SECURE_PROXY_SSL_HEADER"],
            ("HTTP_X_FORWARDED_PROTO", "https"),
        )
        self.assertTrue(production["SESSION_COOKIE_SECURE"])
        self.assertTrue(production["CSRF_COOKIE_SECURE"])
        self.assertFalse(production.get("SECURE_SSL_REDIRECT", False))

    def test_local_http_development_keeps_cookies_usable(self):
        development = self.settings_for("True")

        self.assertTrue(development["DEBUG"])
        self.assertIsNone(development["SECURE_PROXY_SSL_HEADER"])
        self.assertFalse(development["SESSION_COOKIE_SECURE"])
        self.assertFalse(development["CSRF_COOKIE_SECURE"])


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

    @override_settings(
        ALLOWED_HOSTS=["portfolio.example"],
        SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    )
    def test_homepage_metadata_uses_forwarded_https_and_omits_query_string(self):
        response = self.client.get(
            "/?from=linkedin",
            HTTP_HOST="portfolio.example",
            HTTP_X_FORWARDED_PROTO="https",
        )
        html = response.content.decode()
        title = "Miguel Ribeiro | Automation, Software and Cloud"
        description = (
            "Miguel Ribeiro builds automation, data workflows and Python-backed "
            "applications for operational problems."
        )
        canonical = "https://portfolio.example/"

        self.assertTrue(response.wsgi_request.is_secure())
        self.assertInHTML(f"<title>{title}</title>", html)
        self.assertInHTML(f'<meta name="description" content="{description}">', html)
        self.assertInHTML(f'<link rel="canonical" href="{canonical}">', html)
        for property_name, value in (
            ("og:title", title),
            ("og:description", description),
            ("og:url", canonical),
            ("og:type", "website"),
        ):
            self.assertInHTML(
                f'<meta property="{property_name}" content="{value}">', html
            )
        self.assertInHTML('<meta name="twitter:card" content="summary">', html)
        self.assertInHTML(f'<meta name="twitter:title" content="{title}">', html)
        self.assertInHTML(
            f'<meta name="twitter:description" content="{description}">', html
        )

    @override_settings(
        ALLOWED_HOSTS=["portfolio.example"],
        SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    )
    def test_project_metadata_uses_its_own_summary_and_canonical_url(self):
        path = reverse("project_detail", args=[self.project.slug])
        response = self.client.get(
            f"{path}?from=linkedin",
            HTTP_HOST="portfolio.example",
            HTTP_X_FORWARDED_PROTO="https",
        )
        html = response.content.decode()
        title = "Test Project | Miguel Ribeiro"
        canonical = f"https://portfolio.example{path}"

        self.assertInHTML(f"<title>{title}</title>", html)
        self.assertInHTML(
            f'<meta name="description" content="{self.project.summary}">', html
        )
        self.assertInHTML(f'<link rel="canonical" href="{canonical}">', html)
        for property_name, value in (
            ("og:title", title),
            ("og:description", self.project.summary),
            ("og:url", canonical),
            ("og:type", "article"),
        ):
            self.assertInHTML(
                f'<meta property="{property_name}" content="{value}">', html
            )
        self.assertInHTML('<meta name="twitter:card" content="summary">', html)
        self.assertInHTML(f'<meta name="twitter:title" content="{title}">', html)
        self.assertInHTML(
            f'<meta name="twitter:description" content="{self.project.summary}">',
            html,
        )

    def test_skip_link_precedes_navigation_and_targets_main_content(self):
        for path in ("/", reverse("project_detail", args=[self.project.slug])):
            with self.subTest(path=path):
                html = self.client.get(path).content.decode()
                self.assertInHTML(
                    '<a class="skip-link" href="#main-content">Skip to main content</a>',
                    html,
                )
                self.assertIn('<main id="main-content" tabindex="-1">', html)
                self.assertLess(
                    html.index('class="skip-link"'), html.index('class="brand"')
                )

    def test_homepage_shows_project(self):
        response = self.client.get("/")

        self.assertContains(response, "Test Project")

    def test_cv_download_links_point_to_public_pdf(self):
        cv_path = "portfolio/files/miguel-ribeiro-cv.pdf"
        self.assertIsNotNone(finders.find(cv_path))

        cv_link = f'href="{static(cv_path)}" download>Download CV</a>'
        home = self.client.get("/")
        detail = self.client.get(reverse("project_detail", args=[self.project.slug]))

        self.assertEqual(home.content.decode().count(cv_link), 2)
        self.assertContains(detail, cv_link)
        self.assertContains(home, 'href="#projects">View Projects')
        self.assertContains(home, 'href="https://github.com/MiguelRibeiro-Cloud"')
        self.assertContains(home, 'href="https://www.linkedin.com/in/miguel-js-ribeiro/"')

    def test_homepage_presents_portfolio_engineering_after_selected_work(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertLess(html.index('id="projects"'), html.index('id="lab-title"'))
        self.assertLess(html.index('id="lab-title"'), html.index('id="capabilities-title"'))
        self.assertContains(response, "This portfolio is an engineering project.")
        for implemented_detail in (
            "Django and PostgreSQL",
            "idempotent Django management command",
            "Docker Compose",
            "PostgreSQL-backed GitHub Actions CI",
            "Railway deployment",
            "Google Gemini assistant",
            "credentials stay server-side",
        ):
            with self.subTest(implemented_detail=implemented_detail):
                self.assertContains(response, implemented_detail)

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
