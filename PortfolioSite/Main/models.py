from ipaddress import ip_address

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models, transaction
from django.db.models import Deferrable, UniqueConstraint, F, Max
from django.urls import reverse
from django.utils import timezone

from tinymce import models as tinymce_models 
import logging
logger = logging.getLogger(__name__)

# Create your models here.

class Email(models.Model):
    """
    Stores email from contact form in case server unable to send to administrator.
    """
    name = models.CharField(
        verbose_name="Name",
        max_length=200,
    )
    email = models.EmailField(
        verbose_name = "Email",
        max_length=500
    )
    body = models.TextField(
        verbose_name ="Body",
        help_text="4000 Character Limmit",
        max_length = 4000,
    )
    subject = models.CharField(
        verbose_name="Subject",
        max_length = 750,
    )
    submitted_date = models.DateTimeField(
        verbose_name="Submitted At",
        auto_now_add=True,
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Sender IP Address",
    )
    status = models.BooleanField(
        verbose_name="Delivery Status",
        null=True,
        blank=True,
    )

    def forward(self):
        """
        Forwards email to contact form recipient. Returns status
        """
        body = f"""leifkjos.com contact form email:
Name: {self.name}
Email: {self.email}
IP: {self.ip_address}
At: {timezone.localtime()}

Subject: {self.subject}

Message:
{self.body}

"""
        try:
            email = EmailMessage(
                f"Message From {self.email}: {self.subject}",
                body,
                settings.EMAIL_CONTACT_FROM_ADDRESS,
                [settings.EMAIL_CONTACT_TO_ADDRESS],
                reply_to=[self.email]
            )
            status = email.send()
        except Exception as e:
            logger.exception(f'Failed sending contact form email from {self.name} {self.email}, subject: {self.subject}', e.args)
            status = 0
        
        else:
            if status != 1:
                logger.error(f'Failed sending contact form email from {self.name} {self.email}, subject: {self.subject}')
        
        self.status = status
        self.save()
        return self.status

    def __str__(self):
        subj = (self.subject[:75] + '...') if len(self.subject) > 75 else self.subject
        return " - ".join([self.name, subj])

# From https://www.revsys.com/tidbits/keeping-django-model-objects-ordered/
class StepManager(models.Manager):
    """
    Manager to order models
    """

    def move(self, obj, new_order):
        """ Move an object to a new order position """

        qs = self.get_queryset()

        with transaction.atomic():
            if hasattr(obj, 'step_related_to_model'):

                # qs = eval(f"self.filter({step_related_to_model})")
                related_model = apps.get_model(obj.step_related_to_app,obj.step_related_to_model)
                kwgs = {obj.step_related_to_field: obj.pk}
                related_object = related_model.objects.get(**kwgs)
                qs = self.filter(project__pk=related_object.id)
            else:
                qs = self.all()

            if obj.order > int(new_order):
                qs.filter(
                    order__lt=obj.order,
                    order__gte=new_order,
                ).exclude(
                    pk=obj.pk
                ).update(
                    order=F('order') + 1,
                )
            else:
                qs.filter(
                    order__lte=new_order,
                    order__gt=obj.order,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    order=F('order') - 1,
                )

            obj.order = new_order
            obj.save()
    
    def create(self, related_pk=None, **kwargs):
        """ Create a new object in last position"""
        instance = self.model(**kwargs)
        
        with transaction.atomic():
            # Get our current max order number
            if hasattr(instance, 'step_related_to_model'):
                if not related_pk:
                    raise ValueError("Related PK required")
                qs = eval(f"self.filter({instance.step_related_to_model.lower()}__pk={int(related_pk)})")
            else:
                qs = self.all()
            results = qs.aggregate(
                Max('order')
            )

            # Increment and use it for our new object
            current_order = results['order__max']
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            if hasattr(instance, 'step_related_to_model'):
                if not related_pk:
                    raise ValueError("Related PK required")
                related_model = apps.get_model(app_label=instance.step_related_to_app, model_name=instance.step_related_to_model)
                related_obj = related_model.objects.get(pk=related_pk)
                eval(f"related_obj.{instance.step_related_to_field}.add({instance.id})")
                

            return instance

class OrderedModel(models.Model):
    order = models.PositiveSmallIntegerField()
    objects = StepManager()

    class Meta:
        abstract=True

class Image(OrderedModel):
    """
    Stores images for projects
    """
    step_related_to_app = 'Main'
    step_related_to_model = 'Project'
    step_related_to_field = 'images'
    
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/'
    )

    caption = tinymce_models.HTMLField(
        max_length=1500,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return f"{settings.MEDIA_URL}{self.image.url}"

    def __str__(self):
        return str(self.title)

class Embed(OrderedModel):
    title = models.CharField(max_length=200)
    html = models.TextField(
        help_text="Paste embed HTML here. Warning, this will be rendered directly to page as |safe",
        max_length=1500
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

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk':self.pk})
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        constraints=[
            UniqueConstraint(
                name='unique_project_order',
                fields=['order'],
                deferrable=Deferrable.DEFERRED,
            )
        ]
    

