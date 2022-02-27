from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import EmailMessage
from django.db.models import Subquery, OuterRef, Max, F
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views import View
from django.views.generic import TemplateView, DetailView

from Main.forms import ContactForm
from Main.models import Project, Image, Email
from Main.helpers import get_client_ip

from pprint import pprint
import json, logging
logger = logging.getLogger(__name__)

# Create your views here.
class Home(TemplateView):
    """
    Site Home Page
    """
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        sq = Image.objects.filter(project__pk=OuterRef('id')).order_by('order').values('image')
        if self.request.user.is_authenticated:
            project_qs = Project.objects.all()
        else:
            project_qs = Project.objects.filter(published=True)
        context['projects'] = project_qs.order_by('order').annotate(
            first_image = Subquery(sq[:1])
        ).values('pk', 'title', 'first_image')

        return context


class ProjectDetail(UserPassesTestMixin, DetailView):
    """
    ProjectDetail Page
    """
    raise_exception=True
    template_name='portfolio-details.html'
    model=Project

    def test_func(self):
        self.object = self.get_object()
        if not self.object.published:
            if not self.request.user.is_authenticated:
                return False
        return True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        context['images'] = Image.objects.filter(project__id=self.object.id).order_by('order')

        return context

    
#ajax views
mimetype='application/json'

class AjaxMoveBaseView(View):
    model=None

    def put(self, request, **kwargs):
        # print(f'called move ajax for {self.model}')
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'unauthorized'}, status=403)

        try:
            # print(request.body.decode('utf-8'))
            data = json.loads(request.body.decode('utf-8'))

        except json.JSONDecodeError:
            # print('bad data found')
            return JsonResponse({'status': 'bad request'}, status=400) 

        try:
            obj = self.model.objects.get(pk=int(kwargs['pk']))
            order = obj.order
        except self.model.DoesNotExist:
            # print('model not found')
            return JsonResponse({'status': 'not found'}, status=404)

        if data['action'] == 'up':
            if order > 1:
                new_order = order - 1
            else:
                # print('min reached')
                return JsonResponse({'status': 'min already reached'}, status=400)

        elif data['action'] == 'down':
            max_order = self.model.objects.all().aggregate(max=Max(F('order')))
            # print('max order:', max_order['max'])
            # print('all:', self.model.objects.all())
            if order < max_order['max']:
                new_order=order+1
            else:
                print('max reached')
                return JsonResponse({'status': 'max already reached'}, status=400)
        else:
            return JsonResponse({'status': 'bad request'}, status=400) 
        
        self.model.objects.move(obj,new_order)
        # print(f"success, new order: {self.model.objects.all().values('title','order')}")
        return JsonResponse({'status': 'success'}, status=203)

class MoveProject(AjaxMoveBaseView):
    model = Project

class MoveImage(AjaxMoveBaseView):
    model = Image

class Contact(View):
    def post(self, request, **kwargs):
        
        ip = get_client_ip(request)
        form = ContactForm(request.POST, ip_address=ip)
        if form.is_valid():
            email:Email = form.save(commit=False)
            status = email.forward()
            if status == 1:
                return JsonResponse('OK',safe=False,status=200)
            else:
                return JsonResponse('Something Went Wrong',safe=False,status=500)
        else:
            return JsonResponse('Bad Request',safe=False, status=400)
            

            
