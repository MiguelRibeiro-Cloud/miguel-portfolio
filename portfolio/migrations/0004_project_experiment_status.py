from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_project_kind_project_live_url_project_source_url_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="project",
                    name="status",
                    field=models.CharField(
                        choices=[
                            ("production", "Production"),
                            ("prototype", "Prototype"),
                            ("learning", "Learning"),
                            ("experiment", "Experiment"),
                        ],
                        default="prototype",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
