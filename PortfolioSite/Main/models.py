from ipaddress import ip_address
from django.db import models
from tinymce import models as tinymce_models 
from django.conf import settings
from django.urls import reverse

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

    def __str__(self):
        subj = (self.subject[:75] + '...') if len(self.subject) > 75 else self.subject
        return " - ".join([self.name, subj])

class Image(models.Model):
    """
    Stores images for projects
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/'
    )
    order = models.PositiveSmallIntegerField(
        null=True
    )

    def get_absolute_url(self):
        return f"{settings.MEDIA_URL}{self.image.url}"

    def __str__(self):
        return str(self.title)

class Project(models.Model):
    """
    Stores project description
    """
    title = models.CharField(max_length=500)
    description = tinymce_models.HTMLField()
    images = models.ManyToManyField(Image)

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk':self.pk})
    def __str__(self):
        return str(self.title)
