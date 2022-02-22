from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from django.db.models import Max, F
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView
from Main.models import Project, Image
from django.conf import settings
import json

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

        return context

#ajax views
mimetype='application/json'

class AjaxMoveBaseView(View):
    model=None

    def put(self, request, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'unauthorized'}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'bad request'}, status=400) 

        try:
            obj = self.model.objects.get(pk=int(kwargs['pk']))
            order = obj.order
        except self.model.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)

        if data['action'] == 'down':
            if order > 1:
                new_order = order - 1
            else:
                return JsonResponse({'status': 'min already reached'}, status=400)

        elif data['action'] == 'up':
            max_order = self.model.objects.all().aggregate(max=Max(F('order')))
            if order < max_order['max']:
                new_order=order+1
            else:
                return JsonResponse({'status': 'max already reached'}, status=400)
        
        self.model.objects.move(obj,new_order)
        return JsonResponse({'status': 'success'}, status=203)

class MoveProject(AjaxMoveBaseView):
    model = Project

class MoveImage(AjaxMoveBaseView):
    model = Image


            
            
