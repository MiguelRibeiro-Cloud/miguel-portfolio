from django.db import models


class Project(models.Model):
    class Kind(models.TextChoices):
        PROFESSIONAL = "professional", "Professional"
        PERSONAL = "personal", "Personal"
        LEARNING = "learning", "Learning"

    class Status(models.TextChoices):
        PRODUCTION = "production", "Production"
        PROTOTYPE = "prototype", "Prototype"
        LEARNING = "learning", "Learning"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    kind = models.CharField(
        max_length=20,
        choices=Kind.choices,
        default=Kind.PROFESSIONAL,
    )
    summary = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROTOTYPE,
    )

    def __str__(self):
        return self.title


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="screenshots",
    )
    image_path = models.CharField(
        max_length=255,
        help_text="Path under static files, for example portfolio/projects/example.png.",
    )
    caption = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "image_path"],
                name="unique_project_screenshot_path",
            ),
        ]

    def __str__(self):
        return f"{self.project.title}: {self.image_path}"
