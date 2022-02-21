from django.urls import path
from Main import views
from Main.views import move_project

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project'),
    path('ajax/move-project/<int:pk>/', views.move_project, name='move_project'),
    ]