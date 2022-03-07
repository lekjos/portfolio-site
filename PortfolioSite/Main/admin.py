from django.contrib import admin, messages
from django.db.models import F, Max
from Main.models import Email, Image, Embed, Project
# Register your models here.

@admin.action(description='Move Up')
def move_up(modeladmin, request, queryset):
    if len(queryset) > 1:
        messages.error(request, 'Please only select one model')
        return None
    
    obj = queryset.first()

    if obj.order > 1:
        new_order = obj.order - 1
        modeladmin.model.objects.move(obj,new_order)
    else:
        # print('min reached')
        messages.error(request, 'Max already reached')

@admin.action(description='Move Down')
def move_down(modeladmin, request, queryset):
    if len(queryset) > 1:
        messages.error(request, 'Please only select one model')
        return None
    
    obj = queryset.first()

    max_order = modeladmin.model.objects.all().aggregate(max=Max(F('order')))
    # print('max order:', max_order['max'])
    # print('all:', self.model.objects.all())
    if obj.order < max_order['max']:
        new_order=obj.order+1
        modeladmin.model.objects.move(obj,new_order)
    else:
        messages.error(request, 'Min already reached')
    

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','submitted_date']
    search_fields=['email','name','subject']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['title','order']
    list_filter=['order', 'project__title']
    search_fields=['title']
    actions=[move_up,move_down]

@admin.register(Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display=['title','order']
    list_filter=['order']
    search_fields=['title']
    actions=[move_up,move_down]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title','order','published']
    list_filter=['published']
    search_fields=['title']
    prepopulated_fields = {'slug': ('title',)} 
    actions=[move_up,move_down]