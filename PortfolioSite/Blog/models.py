from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from tinymce import models as tinymce_models
# Create your models here.

class Comment(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
        )
    value =  tinymce_models.HTMLField(max_length=1000)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
        )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    value = models.TextField(max_length=100)
    
    def __str__(self):
        return self.value

class Post(models.Model):
    """
    Blog Post
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
        )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = tinymce_models.HTMLField()
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

class Profile(models.Model):
    """
    Profile about the author, tied to user model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="profile"
        )
    bio = tinymce_models.HTMLField()

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"