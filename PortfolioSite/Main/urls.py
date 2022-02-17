from django.urls import path
from Main import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project')
    ]