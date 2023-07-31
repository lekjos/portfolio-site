import logging

from django.apps import apps
from django.db import models, transaction
from django.db.models import Deferrable, F, Max, UniqueConstraint
from django.template.defaultfilters import slugify
from django.urls import reverse
from tinymce import models as tinymce_models

logger = logging.getLogger(__name__)

# Create your models here.


# From https://www.revsys.com/tidbits/keeping-django-model-objects-ordered/
class StepManager(models.Manager):
    """
    Manager to order models
    """

    def move(self, obj, new_order):
        """Move an object to a new order position"""

        qs = self.get_queryset()

        with transaction.atomic():
            if hasattr(obj, "step_related_to_model"):
                # qs = eval(f"self.filter({step_related_to_model})")
                related_model = apps.get_model(
                    obj.step_related_to_app, obj.step_related_to_model
                )
                kwgs = {obj.step_related_to_field: obj.pk}
                related_object = related_model.objects.get(**kwgs)
                qs = self.filter(project__pk=related_object.id)
            else:
                qs = self.all()

            if obj.order > int(new_order):
                qs.filter(
                    order__lt=obj.order,
                    order__gte=new_order,
                ).exclude(pk=obj.pk).update(
                    order=F("order") + 1,
                )
            else:
                qs.filter(
                    order__lte=new_order,
                    order__gt=obj.order,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    order=F("order") - 1,
                )

            obj.order = new_order
            obj.save()

    def create(self, related_pk=None, **kwargs):
        """Create a new object in last position"""
        instance = self.model(**kwargs)

        with transaction.atomic():
            # Get our current max order number
            if hasattr(instance, "step_related_to_model"):
                if not related_pk:
                    raise ValueError("Related PK required")
                qs = eval(
                    f"self.filter({instance.step_related_to_model.lower()}__pk={int(related_pk)})"
                )
            else:
                qs = self.all()
            results = qs.aggregate(Max("order"))

            # Increment and use it for our new object
            current_order = results["order__max"]
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            if hasattr(instance, "step_related_to_model"):
                if not related_pk:
                    raise ValueError("Related PK required")
                related_model = apps.get_model(
                    app_label=instance.step_related_to_app,
                    model_name=instance.step_related_to_model,
                )
                related_obj = related_model.objects.get(pk=related_pk)
                eval(f"related_obj.{instance.step_related_to_field}.add({instance.id})")

            return instance


class OrderedModel(models.Model):
    order = models.PositiveSmallIntegerField()
    objects = StepManager()

    class Meta:
        abstract = True


class Image(OrderedModel):
    """
    Stores images for projects
    """

    step_related_to_app = "Main"
    step_related_to_model = "Project"
    step_related_to_field = "images"

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")

    caption = tinymce_models.HTMLField(
        max_length=1500,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return f"{self.image.url}"

    def __str__(self):
        return str(self.title)


class Embed(OrderedModel):
    title = models.CharField(max_length=200)
    html = models.TextField(
        help_text="Paste embed HTML here. Warning, this will be rendered directly to page as |safe",
        max_length=1500,
    )

    def __str__(self):
        return str(self.title)


class Project(OrderedModel):
    """
    Stores project description
    """

    title = models.CharField(max_length=500)
    description = tinymce_models.HTMLField()
    images = models.ManyToManyField(Image, blank=True)
    embeds = models.ManyToManyField(Embed, blank=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, null=True, unique=True, blank=True)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=750, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("project", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_project_order",
                fields=["order"],
                deferrable=Deferrable.DEFERRED,
            )
        ]
