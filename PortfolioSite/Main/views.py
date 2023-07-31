import json
import logging
from itertools import chain

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import F, Max, OuterRef, Subquery
from django.http import (
    JsonResponse,
)
from django.views import View
from django.views.generic import DetailView, TemplateView
from Main.helpers import find_next_and_previous
from Main.models import Embed, Image, Project

logger = logging.getLogger(__name__)


# Create your views here.
class Home(TemplateView):
    """
    Site Home Page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_url"] = settings.MEDIA_URL
        sq = (
            Image.objects.filter(project__pk=OuterRef("id"))
            .order_by("order")
            .values("image")
        )
        if self.request.user.is_authenticated:
            project_qs = Project.objects.all()
        else:
            project_qs = Project.objects.filter(published=True)
        context["projects"] = (
            project_qs.order_by("order")
            .annotate(first_image=Subquery(sq[:1]))
            .values("pk", "slug", "title", "first_image")
        )
        context["project_slugs"] = [x["slug"] for x in context["projects"]]
        return context


class ProjectDetail(UserPassesTestMixin, DetailView):
    """
    ProjectDetail Page
    """

    raise_exception = True
    template_name = "portfolio-details.html"
    model = Project

    def test_func(self):
        """
        Hides unpublished objects
        """
        if not hasattr(self, "object"):
            self.object = self.get_object()
        if not self.object.published:
            if not self.request.user.is_authenticated:
                return False
        return True

    def get(self, request, *args, **kwargs):
        ## Don't get object if already fetched in test_func
        if not hasattr(self, "object"):
            self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_url"] = settings.MEDIA_URL
        context["images"] = (
            Image.objects.filter(project__slug=self.object.slug)
            .order_by("order")
            .values("image", "order", "title")
        )
        context["embeds"] = (
            Embed.objects.filter(project__slug=self.object.slug)
            .order_by("order")
            .values("html", "title")
        )
        context["enable_swiper"] = (
            True
            if len(list(chain(context["images"], context["embeds"]))) > 1
            else False
        )
        context["enable_jquery"] = True
        context["page_title"] = self.object.title
        context["page_description"] = self.object.short_description

        project_qs = (
            Project.objects.filter(published=True)
            .order_by("order")
            .values("slug", "title", "order")
        )
        r = find_next_and_previous(self.object.slug, project_qs)
        context = context | r

        return context


# ajax views
mimetype = "application/json"


class AjaxMoveBaseView(View):
    model = None

    def put(self, request, **kwargs):
        # print(f'called move ajax for {self.model}')
        if not request.user.is_authenticated:
            return JsonResponse({"status": "unauthorized"}, status=403)

        try:
            # print(request.body.decode('utf-8'))
            data = json.loads(request.body.decode("utf-8"))

        except json.JSONDecodeError:
            # print('bad data found')
            return JsonResponse({"status": "bad request"}, status=400)

        try:
            if "slug" in kwargs:
                obj = self.model.objects.get(slug=kwargs["slug"])
            elif "pk" in kwargs:
                obj = self.model.objects.get(pk=int(kwargs["pk"]))
            else:
                return JsonResponse({"status": "bad request"}, status=400)
            order = obj.order
        except self.model.DoesNotExist:
            # print('model not found')
            return JsonResponse({"status": "not found"}, status=404)

        if data["action"] == "up":
            if order > 1:
                new_order = order - 1
            else:
                # print('min reached')
                return JsonResponse({"status": "min already reached"}, status=400)

        elif data["action"] == "down":
            max_order = self.model.objects.all().aggregate(max=Max(F("order")))
            # print('max order:', max_order['max'])
            # print('all:', self.model.objects.all())
            if order < max_order["max"]:
                new_order = order + 1
            else:
                return JsonResponse({"status": "max already reached"}, status=400)
        else:
            return JsonResponse({"status": "bad request"}, status=400)

        self.model.objects.move(obj, new_order)
        # print(f"success, new order: {self.model.objects.all().values('title','order')}")
        return JsonResponse({"status": "success"}, status=203)


class MoveProject(AjaxMoveBaseView):
    model = Project


class MoveImage(AjaxMoveBaseView):
    model = Image
