# Generated by Django 4.0.2 on 2022-03-01 05:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Main", "0010_alter_embed_html"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="embeds",
            field=models.ManyToManyField(blank=True, to="Main.Embed"),
        ),
        migrations.AlterField(
            model_name="project",
            name="images",
            field=models.ManyToManyField(blank=True, to="Main.Image"),
        ),
    ]
