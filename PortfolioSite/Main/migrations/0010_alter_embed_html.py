# Generated by Django 4.0.2 on 2022-03-01 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_embed_project_embeds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embed',
            name='html',
            field=models.TextField(help_text='Paste embed HTML here. Warning, this will be rendered directly to page as |safe', max_length=1500),
        ),
    ]