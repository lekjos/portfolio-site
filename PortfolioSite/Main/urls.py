from django.urls import path
from Main import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project'),
    path('ajax/move-project/<int:pk>/', views.MoveProject.as_view(), name='move_project'),
    path('ajax/move-image/<int:pk>/', views.MoveImage.as_view(), name='move_image'),
    path('ajax/contact/', views.Contact.as_view(), name='contact'),
    ]