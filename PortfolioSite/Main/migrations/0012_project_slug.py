# Generated by Django 4.0.2 on 2022-03-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Main", "0011_alter_project_embeds_alter_project_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(max_length=250, null=True, unique=True, blank=True),
        ),
    ]
