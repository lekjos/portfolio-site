from ipaddress import ip_address
from django.db import models

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
        auto_created=True,
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Sender IP Address",
    )

    def __str__(self):
        subj = (self.subject[:75] + '...') if len(self.subject) > 75 else self.subject
        return " - ".join([self.name, subj])