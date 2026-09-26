"""Synchronize version-controlled public project content on demand."""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from portfolio.content.projects import PROJECTS
from portfolio.models import Project, ProjectScreenshot


class Command(BaseCommand):
    help = "Create or update portfolio projects from version-controlled content."

    def handle(self, *args, **options):
        results = []

        with transaction.atomic():
            for project in PROJECTS:
                slug = project["slug"]
                screenshots = project.get("screenshots", ())
                if project["kind"] == Project.Kind.PROFESSIONAL and screenshots:
                    raise CommandError(
                        f"Professional project {slug} cannot have screenshots."
                    )

                defaults = {
                    key: value
                    for key, value in project.items()
                    if key not in ("slug", "screenshots")
                }
                record, created = Project.objects.update_or_create(
                    slug=slug,
                    defaults=defaults,
                )
                configured_paths = []
                for screenshot in screenshots:
                    configured_paths.append(screenshot["image_path"])
                    ProjectScreenshot.objects.update_or_create(
                        project=record,
                        image_path=screenshot["image_path"],
                        defaults={
                            "caption": screenshot.get("caption", ""),
                            "sort_order": screenshot.get("sort_order", 0),
                        },
                    )
                record.screenshots.exclude(
                    image_path__in=configured_paths
                ).delete()
                results.append((project["title"], created))

        for title, created in results:
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action}: {title}")
