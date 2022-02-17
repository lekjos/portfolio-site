from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.db.models import Subquery, OuterRef
from Main.models import Project, Image
from django.conf import settings

# Create your views here.
class Home(TemplateView):
    """
    Site Home Page
    """
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        sq = Image.objects.filter(pk=OuterRef('id')).order_by('order').values('image')
        context['projects'] = Project.objects.all().annotate(
            first_image = Subquery(sq[:1])
        ).values('pk', 'title', 'first_image')

        return context

class ProjectDetail(DetailView):
    """
    ProjectDetail Page
    """
    template_name='portfolio-details.html'
    model=Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        context['images'] = Image.objects.filter(project__id=self.object.id)
        print(context['images'].first().image.url)

        return context

