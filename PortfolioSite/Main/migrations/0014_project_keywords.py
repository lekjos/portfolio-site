# Generated by Django 4.0.2 on 2022-03-08 00:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Main", "0013_project_short_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="keywords",
            field=models.CharField(blank=True, max_length=750, null=True),
        ),
    ]
