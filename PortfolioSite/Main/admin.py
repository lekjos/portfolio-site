from django.contrib import admin
from Main.models import Email, Image, Project
# Register your models here.

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','submitted_date']
    search_fields=['email','name','subject']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['title']
    search_fields=['title']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title']
    search_fields=['title']