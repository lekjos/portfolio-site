from django.urls import path
from Main import views
from django.views.generic.base import TemplateView #import TemplateView


urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('projects/<slug:slug>/', views.ProjectDetail.as_view(), name='project'),
    path('ajax/move-project/<int:pk>/', views.MoveProject.as_view(), name='move_project'),
    path('ajax/move-image/<int:pk>/', views.MoveImage.as_view(), name='move_image'),
    path('ajax/contact/', views.Contact.as_view(), name='contact'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt',content_type="text/plain")),

    ]