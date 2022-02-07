from django.urls import path
from Main import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    ]