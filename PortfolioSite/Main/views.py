from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

# Create your views here.
class Home(TemplateView):
    """
    Site Home Page
    """
    template_name='index.html'