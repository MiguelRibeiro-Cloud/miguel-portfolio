from django.db import models


class Project(models.Model):
    class Status(models.TextChoices):
        PRODUCTION = "production", "Production"
        PROTOTYPE = "prototype", "Prototype"
        LEARNING = "learning", "Learning"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROTOTYPE,
    )

    def __str__(self):
        return self.title