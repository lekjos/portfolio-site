from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from Main.models import Project

# Create your views here.
class Home(TemplateView):
    """
    Site Home Page
    """
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all().values('title','images__image')

        return context

