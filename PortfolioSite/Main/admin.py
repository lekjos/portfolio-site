from django.contrib import admin
from Main.models import Email, Image, Embed, Project
# Register your models here.

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','submitted_date']
    search_fields=['email','name','subject']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['title','order']
    list_filter=['order']
    search_fields=['title']

@admin.register(Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display=['title','order']
    list_filter=['order']
    search_fields=['title']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title','order','published']
    list_filter=['published']
    search_fields=['title']